"""Generate the adopted S1 exposure report (fourth relay, double consent).

Descriptive only: realized intervened-site counts per (family, depth) cell
per arm, published beside the frozen density metric, never used as a
denominator for the primary estimands. Computes no accuracy quantity, so it
is safe to run before any outcome ruling.

    python scripts/s1_exposure_report.py --out runs/s1_exposure.json
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_arm(armdir: str):
    for fn in sorted(os.listdir(armdir)):
        if not fn.endswith(".jsonl"):
            continue
        with open(os.path.join(armdir, fn), encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=os.path.join(REPO, "runs"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    arms = sorted(d for d in os.listdir(args.runs_dir)
                  if d.startswith("randomized-")
                  and os.path.isdir(os.path.join(args.runs_dir, d)))

    report: dict = {"arms": {}, "rule_totals": {}, "skip_totals": {}}
    rule_intervened: Counter = Counter()
    rule_decided: Counter = Counter()
    skips: Counter = Counter()

    for arm in arms:
        cells = defaultdict(list)
        for rec in load_arm(os.path.join(args.runs_dir, arm)):
            k = 0
            for s in rec.get("sites", []):
                rule_decided[s["rule_id"]] += 1
                if s.get("intervened"):
                    rule_intervened[s["rule_id"]] += 1
                    k += 1
                if s.get("skip_reason"):
                    skips[s["skip_reason"]] += 1
            cells[f'{rec["family"]}:d{rec["depth"]}'].append(k)

        arm_report = {}
        for cell, ks in sorted(cells.items()):
            ks_sorted = sorted(ks)
            n = len(ks_sorted)
            median = (ks_sorted[n // 2] if n % 2 == 1
                      else (ks_sorted[n // 2 - 1] + ks_sorted[n // 2]) / 2)
            arm_report[cell] = {
                "n_problems": n,
                "mean_intervened_per_trace": sum(ks_sorted) / n,
                "median_intervened_per_trace": median,
                "distribution": {str(k): c for k, c in
                                 sorted(Counter(ks_sorted).items())},
                "problems_with_at_least_one": sum(1 for k in ks_sorted if k > 0),
                "coverage_fraction": sum(1 for k in ks_sorted if k > 0) / n,
            }
        report["arms"][arm] = arm_report

    report["rule_totals"] = {
        r: {"sites_decided": rule_decided[r], "sites_intervened": rule_intervened[r]}
        for r in sorted(set(rule_decided) | set(rule_intervened))
    }
    report["skip_totals"] = dict(sorted(skips.items(), key=lambda kv: -kv[1]))
    report["_note"] = (
        "S1 exposure reporting, adopted by double consent (fourth relay). "
        "Descriptive only; never a denominator for primary estimands. "
        "Rules with zero interventions are structurally unavailable, not null "
        "effects (Sol, sixth relay)."
    )

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"S1 exposure report -> {args.out}")
    print(f"arms: {len(report['arms'])}; "
          f"total intervened: {sum(rule_intervened.values())}; "
          f"total decided: {sum(rule_decided.values())}")


if __name__ == "__main__":
    main()
