"""Diagnostic: decompose the rule-05 (whitespace) accuracy penalty.

Distinguishes a REASONING failure (model emits a wrong number) from a
GENERATION-TERMINATION artifact (model stops before emitting a parseable
ANSWER line). Run after scripts/run_analysis.py.

    python scripts/diagnose_whitespace.py --cell multiplication-d2
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDS = ["271828", "161803", "141421"]


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def profile(label: str, recs: list[dict]) -> dict:
    n = max(len(recs), 1)
    row = {
        "n": len(recs),
        "correct": sum(1 for r in recs if r["correct"]),
        "wrong_number": sum(1 for r in recs
                            if r["answer_extracted"] is not None and not r["correct"]),
        "no_answer": sum(1 for r in recs if r["answer_extracted"] is None),
        "mean_tokens": sum(r["generated_tokens"] for r in recs) / n,
        "ended": dict(Counter(r["ended"] for r in recs)),
    }
    print(f"{label:<32} n={row['n']:<5} correct={row['correct']:<5} "
          f"wrong={row['wrong_number']:<5} NO_ANSWER={row['no_answer']:<5} "
          f"tokens={row['mean_tokens']:>6.0f}")
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=os.path.join(REPO, "runs"))
    ap.add_argument("--cell", default="multiplication-d2")
    ap.add_argument("--arm", default="tier_a_05_whitespace")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    report = {"cell": args.cell, "arm": args.arm, "seeds": {}}
    print(f"=== {args.cell} / {args.arm} ===")
    report["native"] = profile(
        "native", load(os.path.join(args.runs_dir, "native", args.cell + ".jsonl")))

    for seed in SEEDS:
        d = os.path.join(args.runs_dir,
                         f"randomized-{args.arm}-s{seed}", args.cell + ".jsonl")
        if not os.path.exists(d):
            continue
        recs = load(d)
        touched = [r for r in recs
                   if any(s.get("intervened") for s in r.get("sites", []))]
        untouched = [r for r in recs
                     if not any(s.get("intervened") for s in r.get("sites", []))]
        report["seeds"][seed] = {
            "touched": profile(f"s{seed} touched", touched),
            "untouched": profile(f"s{seed} untouched", untouched),
        }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"-> {args.out}")


if __name__ == "__main__":
    main()
