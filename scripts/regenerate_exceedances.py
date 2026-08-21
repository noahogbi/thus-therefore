"""Exceedance protocol execution (REVIEW_LOG 10B, merged Fable a / Sol 3).

For each RESUMED record carrying a certification exceedance: one full
from-scratch regeneration under the fixed decoder; certify its ENTIRE
generated region at the frozen epsilon; on pass, the regeneration replaces
the resumed record (provenance updated); on fail, the record is EXCLUDED
and tallied. Control-sample exceedances receive no record action (they are
original data; their identical cross-arm replication documents the
instrument's canonical-tokenization artifact rate) but are reported.

Usage (GPU): python scripts/regenerate_exceedances.py --rung followon
"""

from __future__ import annotations

import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from scripts.repair_resume import RUNGS, LOOKAHEAD_CHARS, MAX_NEW_TOKENS, \
    load, make_lm, rules_of  # noqa: E402
from scripts.certify_greedy_consistency import EPSILON, deficits_for  # noqa: E402


def main() -> None:
    import torch
    from harness.runner import run_problems

    ap = argparse.ArgumentParser()
    ap.add_argument("--rung", choices=list(RUNGS), required=True)
    args = ap.parse_args()
    cfg = RUNGS[args.rung]

    cert = json.load(open(os.path.join(
        REPO, "runs", "corrected", f"certification_{args.rung}.json"),
        encoding="utf-8"))
    targets = {}
    for e in cert["resumed"]["exceedances"]:
        targets.setdefault((e["arm"], e["cell"], e["index"]), []).append(e)
    if not targets:
        print(f"[{args.rung}] no resumed exceedances")
        return

    lm = make_lm(cfg)
    outcome = []
    for (arm, cell, idx), excs in sorted(targets.items()):
        path = os.path.join(REPO, cfg["out"], arm, cell + ".jsonl")
        rows = load(path)
        r = rows[idx]
        prob = {"id": r["id"], "family": r["family"], "depth": r["depth"],
                "answer": r["answer_expected"],
                "prompt": r["text"][:r["prompt_chars"]]}
        [fresh] = list(run_problems(
            lm, [prob], mode="randomized", seed=r["seed"],
            rules=rules_of(r), max_new_tokens=MAX_NEW_TOKENS,
            lookahead_chars=LOOKAHEAD_CHARS,
            extended_extraction=cfg["extended_extraction"]))
        rows_def, _ = deficits_for(lm, torch, fresh["text"], fresh["prompt_chars"])
        worst = max((d["deficit"] for d in rows_def), default=0.0)
        ok = worst <= EPSILON
        rec = {"arm": arm, "cell": cell, "index": idx, "id": r["id"],
               "regeneration_worst_deficit": worst,
               "action": "replaced" if ok else "EXCLUDED"}
        if ok:
            fresh["repair"] = {"resumed": False,
                               "regenerated_after_exceedance": True,
                               "prior_exceedances": excs}
            rows[idx] = fresh
        else:
            r["repair"]["excluded_after_exceedance"] = True
            r["repair"]["exceedances"] = excs
            rows[idx] = r
        with open(path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
        outcome.append(rec)
        print(f"[{args.rung}] {arm}/{cell}#{idx}: worst={worst:.3f} -> {rec['action']}", flush=True)

    json.dump(outcome, open(os.path.join(
        REPO, "runs", "corrected", f"exceedance_outcome_{args.rung}.json"),
        "w", encoding="utf-8"), indent=1)
    print(f"[{args.rung}] EXCEEDANCE-PROTOCOL-DONE "
          f"replaced={sum(1 for o in outcome if o['action']=='replaced')} "
          f"excluded={sum(1 for o in outcome if o['action']=='EXCLUDED')}", flush=True)


if __name__ == "__main__":
    main()
