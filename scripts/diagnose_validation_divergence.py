"""Diagnose validation mismatches: locate first divergence relative to the
splice and measure the logit margin at the divergence point.

Discriminates two explanations for a failed from-scratch identity check:
  PREFIX divergence (before the splice): the from-scratch replay departs
    from the ORIGINAL logged trace on this host — evidence about cross-host
    greedy stability of the original run, not about the resume logic (the
    resume never recomputes the prefix).
  TAIL divergence (at/after the splice): the resumed continuation differs
    from what from-scratch produces from the same splice state — evidence
    AGAINST the resume-state equivalence claim.

For each analyzed record also reports the top-2 logit margin at the
divergence position: a near-tie margin is the signature of floating-point
nondeterminism across hosts; a wide margin is not explicable that way.

Diagnostic only; decides nothing. Output goes to the parties.

Usage (GPU box):
  python scripts/diagnose_validation_divergence.py --rung followon --limit 25
"""

from __future__ import annotations

import argparse
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.insert(0, REPO)

from scripts.repair_resume import RUNGS, LOOKAHEAD_CHARS, MAX_NEW_TOKENS, \
    load, make_lm, rules_of  # noqa: E402


def main() -> None:
    import torch
    from harness.runner import run_problems

    ap = argparse.ArgumentParser()
    ap.add_argument("--rung", choices=list(RUNGS), required=True)
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()
    cfg = RUNGS[args.rung]

    report = json.load(open(os.path.join(
        REPO, "runs", "corrected", f"validation_report_{args.rung}.json"),
        encoding="utf-8"))
    fails = [r for r in report["records"] if not r["identical"]][:args.limit]
    lm = make_lm(cfg)

    out = []
    for item in fails:
        f_orig = os.path.join(REPO, cfg["grid"], item["arm"], item["cell"] + ".jsonl")
        f_corr = os.path.join(REPO, cfg["out"], item["arm"], item["cell"] + ".jsonl")
        orig = load(f_orig)[item["index"]]
        corr = load(f_corr)[item["index"]]
        splice = len(orig["text"])  # chop => original text ends at splice
        prob = {"id": orig["id"], "family": orig["family"],
                "depth": orig["depth"], "answer": orig["answer_expected"],
                "prompt": orig["text"][:orig["prompt_chars"]]}
        [scratch] = list(run_problems(
            lm, [prob], mode="randomized", seed=orig["seed"],
            rules=rules_of(orig), max_new_tokens=MAX_NEW_TOKENS,
            lookahead_chars=LOOKAHEAD_CHARS,
            extended_extraction=cfg["extended_extraction"]))
        a, b = scratch["text"], corr["text"]
        div = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y),
                   min(len(a), len(b)) if a != b else -1)
        row = {"id": orig["id"], "arm": item["arm"], "cell": item["cell"],
               "index": item["index"], "splice_char": splice,
               "first_divergence_char": div,
               "region": ("identical" if div == -1 else
                          "prefix" if div < splice else "tail")}
        if div >= 0:
            # logit margin at the divergence: condition on the COMMON prefix
            common = a[:div]
            ids = lm.encode(common)
            with torch.no_grad():
                logits = lm.model(torch.tensor([ids], device=lm.device)).logits[0, -1].float()
            top2 = torch.topk(logits, 2)
            row["top2_margin_logits"] = float(top2.values[0] - top2.values[1])
            row["top2_tokens"] = [lm.tok.decode([int(i)]) for i in top2.indices]
            row["scratch_char"] = a[div:div + 20]
            row["corrected_char"] = b[div:div + 20]
        out.append(row)
        print(f"{row['id']} {row['region']} div@{div} splice@{splice} "
              f"margin={row.get('top2_margin_logits', '-')}")

    path = os.path.join(REPO, "runs", "corrected",
                        f"divergence_diagnosis_{args.rung}.json")
    json.dump(out, open(path, "w", encoding="utf-8"), indent=1)
    regions = {}
    for r in out:
        regions[r["region"]] = regions.get(r["region"], 0) + 1
    print(f"SUMMARY {args.rung}: {regions} -> {path}")


if __name__ == "__main__":
    main()
