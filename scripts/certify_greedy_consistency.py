"""Greedy-consistency certification (relay 10B, unanimous 10B.1(i)).

Supersedes the byte-identity gate. For every RESUMED tail token — and for
matched-size random samples of native and untouched-randomized records —
teacher-force the trace and record, at each certified position, the token's
rank and logit deficit versus the contemporaneously recomputed argmax.

FROZEN PARAMETERS (REVIEW_LOG 10B):
  epsilon = 2.0 logits, derived outcome-blind from the divergence-diagnosis
  margin distribution (ULP-scale mass max 1.875; outliers 3.375/6.75 not
  grandfathered). A deficit <= epsilon is greedy-consistent; deficit 0.000
  is an exact tie (argmax undefined; either branch consistent; the stack
  breaks ties toward the lowest token index in torch.argmax).

Exceedance protocol: exceedances are REPORTED and analysis halts for the
affected rung pending diagnosis (Sol 3 / Fable a); this script never
excludes or repairs records on its own.

Tokenization-boundary accounting: certified regions are addressed in the
canonical tokenization of the full text. Where the canonical encoding of
the region boundary prefix does not round-trip (BPE merge across the
boundary), the boundary is shifted back to the last agreeing token and the
shift is counted and published.

Usage (GPU): python scripts/certify_greedy_consistency.py --rung followon
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from scripts.repair_resume import RUNGS, load, make_lm  # noqa: E402

EPSILON = 2.0
SAMPLE_SEED = "certify:314159"


def certified_positions(lm, text: str, region_start_char: int):
    """Token positions covering text[region_start_char:], canonical ids."""
    full = lm.encode(text)
    prefix = lm.encode(text[:region_start_char])
    boundary = len(prefix)
    shift = 0
    while boundary > 0 and full[:boundary] != prefix[:boundary]:
        boundary -= 1
        shift += 1
    return full, boundary, shift


def deficits_for(lm, torch, text: str, region_start_char: int):
    full, boundary, shift = certified_positions(lm, text, region_start_char)
    if len(full) <= boundary:
        return [], shift
    ids = torch.tensor([full], device=lm.device)
    with torch.no_grad():
        logits = lm.model(ids).logits[0].float()
    rows = []
    for pos in range(boundary, len(full)):
        row = logits[pos - 1]
        tok = full[pos]
        top = torch.topk(row, 5)
        deficit = float(top.values[0] - row[tok])
        rank = int((row > row[tok]).sum().item()) + 1
        rows.append({"pos": pos, "deficit": deficit, "rank": rank})
    return rows, shift


def main() -> None:
    import torch

    ap = argparse.ArgumentParser()
    ap.add_argument("--rung", choices=list(RUNGS), required=True)
    args = ap.parse_args()
    cfg = RUNGS[args.rung]
    lm = make_lm(cfg)
    rng = random.Random(f"{SAMPLE_SEED}:{args.rung}")

    resumed, native_pool, untouched_pool = [], [], []
    for f in sorted(glob.glob(os.path.join(REPO, cfg["out"], "*", "*.jsonl"))):
        arm = os.path.basename(os.path.dirname(f))
        for i, r in enumerate(load(f)):
            if r.get("repair", {}).get("resumed"):
                resumed.append((arm, os.path.basename(f)[:-6], i, r))
            elif any(s.get("intervened") for s in r.get("sites", [])):
                pass  # touched but not resumed: mid-generation, in untouched_pool? no — leave to untouched sample of clean records
            else:
                untouched_pool.append((arm, os.path.basename(f)[:-6], i, r))
    native_dir = os.path.join(REPO, cfg["grid"], "native")
    for f in sorted(glob.glob(os.path.join(native_dir, "*.jsonl"))):
        for i, r in enumerate(load(f)):
            native_pool.append(("native", os.path.basename(f)[:-6], i, r))

    n = len(resumed)
    native_sample = rng.sample(native_pool, min(n, len(native_pool)))
    untouched_sample = rng.sample(untouched_pool, min(n, len(untouched_pool)))

    def certify(group, records, region_fn):
        out = {"group": group, "records": 0, "tokens": 0, "exact_ties": 0,
               "exceedances": [], "boundary_shifts": 0,
               "deficit_hist": {}, "rank_hist": {}}
        for arm, cell, idx, r in records:
            region = region_fn(r)
            rows, shift = deficits_for(lm, torch, r["text"], region)
            out["records"] += 1
            out["boundary_shifts"] += (1 if shift else 0)
            for row in rows:
                out["tokens"] += 1
                d = row["deficit"]
                b = ("0.000" if d == 0.0 else
                     "(0,0.5]" if d <= 0.5 else "(0.5,1]" if d <= 1.0 else
                     "(1,2]" if d <= EPSILON else ">2")
                out["deficit_hist"][b] = out["deficit_hist"].get(b, 0) + 1
                rk = str(min(row["rank"], 5))
                out["rank_hist"][rk] = out["rank_hist"].get(rk, 0) + 1
                if d == 0.0:
                    out["exact_ties"] += 1
                if d > EPSILON:
                    out["exceedances"].append(
                        {"arm": arm, "cell": cell, "index": idx,
                         "id": r["id"], "pos": row["pos"],
                         "deficit": d, "rank": row["rank"]})
            if out["records"] % 250 == 0:
                print(f"  [{group}] {out['records']} records...", flush=True)
        return out

    results = {
        "rung": args.rung, "epsilon": EPSILON,
        "resumed": certify("resumed", resumed,
                           lambda r: r["repair"]["original_len"]),
        "native_sample": certify("native", native_sample,
                                 lambda r: r["prompt_chars"]),
        "untouched_sample": certify("untouched", untouched_sample,
                                    lambda r: r["prompt_chars"]),
    }
    n_exc = sum(len(results[g]["exceedances"])
                for g in ("resumed", "native_sample", "untouched_sample"))
    results["verdict"] = ("PASS" if n_exc == 0 else
                          "EXCEEDANCES_REPORTED_ANALYSIS_HALTED")
    path = os.path.join(REPO, "runs", "corrected",
                        f"certification_{args.rung}.json")
    json.dump(results, open(path, "w", encoding="utf-8"), indent=1)
    for g in ("resumed", "native_sample", "untouched_sample"):
        r = results[g]
        print(f"[{args.rung}] {g}: {r['records']} records, {r['tokens']} tokens, "
              f"ties {r['exact_ties']}, exceedances {len(r['exceedances'])}, "
              f"hist {r['deficit_hist']}", flush=True)
    print(f"[{args.rung}] VERDICT: {results['verdict']} -> {path}", flush=True)


if __name__ == "__main__":
    main()
