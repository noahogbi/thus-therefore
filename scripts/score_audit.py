"""Join audit verdicts to the provenance key and score per-rule pass rates
against the frozen 98% threshold (SPEC section 8, FREEZE.md item 7).

Blinding is preserved by construction: this join happens only after all
verdicts are collected. Output mirrors the rung 1 RESULTS.md table.

Usage:
    python scripts/score_audit.py --verdicts runs/followon/audit_verdicts.jsonl \
        --key runs/followon/audit_key.jsonl --out runs/followon/audit_scored.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict

THRESHOLD = 0.98  # frozen


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verdicts", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    verdicts = {r["audit_id"]: r for r in
                (json.loads(l) for l in open(args.verdicts, encoding="utf-8") if l.strip())}
    key = [json.loads(l) for l in open(args.key, encoding="utf-8") if l.strip()]

    per_rule = defaultdict(lambda: {"n": 0, "pass": 0, "fail": 0, "unparsed": 0,
                                    "failed_criteria": defaultdict(int),
                                    "fail_audit_ids": []})
    total = {"n": 0, "pass": 0, "fail": 0, "unparsed": 0}

    for k in key:
        row = verdicts.get(k["audit_id"])
        rule = k["rule_id"]
        bucket = per_rule[rule]
        bucket["n"] += 1
        total["n"] += 1
        v = (row or {}).get("verdict")
        if not v or "verdict" not in v:
            bucket["unparsed"] += 1
            total["unparsed"] += 1
            continue
        if v["verdict"] == "PASS":
            bucket["pass"] += 1
            total["pass"] += 1
        else:
            bucket["fail"] += 1
            total["fail"] += 1
            bucket["fail_audit_ids"].append(k["audit_id"])
            for c in v.get("failed_criteria", []):
                bucket["failed_criteria"][c] += 1

    result = {"threshold": THRESHOLD, "rules": {}, "total": total,
              "rules_below_threshold": []}
    print(f"{'rule':40s} {'n':>5s} {'pass':>5s} {'rate':>8s}")
    for rule in sorted(per_rule):
        b = per_rule[rule]
        judged = b["pass"] + b["fail"]
        rate = b["pass"] / judged if judged else None
        result["rules"][rule] = {
            "n": b["n"], "pass": b["pass"], "fail": b["fail"],
            "unparsed": b["unparsed"], "rate": rate,
            "failed_criteria": dict(b["failed_criteria"]),
            "fail_audit_ids": b["fail_audit_ids"],
        }
        flag = ""
        if rate is not None and rate < THRESHOLD:
            result["rules_below_threshold"].append(rule)
            flag = "  << BELOW 98% — rule removal + rerun per FREEZE.md item 7"
        print(f"{rule:40s} {b['n']:5d} {b['pass']:5d} "
              f"{(f'{rate*100:.1f}%' if rate is not None else 'n/a'):>8s}{flag}")

    judged_total = total["pass"] + total["fail"]
    overall = total["pass"] / judged_total if judged_total else None
    result["overall_rate"] = overall
    print(f"{'ALL':40s} {total['n']:5d} {total['pass']:5d} "
          f"{(f'{overall*100:.1f}%' if overall is not None else 'n/a'):>8s}")
    if total["unparsed"]:
        print(f"unparsed verdicts: {total['unparsed']} (must be zero or re-judged)")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
