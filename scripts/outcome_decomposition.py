"""Adopted supplementary decompositions (seventh relay, both parties).

7.2 (consent, Sol's three-way form): per arm and cell, split outcomes into
    correct / wrong parseable answer / no parseable answer. The frozen O1 is
    unchanged — no-answer traces remain incorrect.

7.1 (d, both parties): a supplementary aggregate EXCLUDING rule 05, labeled
    a mechanistic decomposition and never a substitute for the frozen
    aggregate. Computed from the independent per-rule arms (mean of their
    O1s), which avoids conditioning on which rules happened to fire inside
    the aggregate arm — that would be post-treatment conditioning of the
    kind Sol objected to in the fourth relay.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDS = ["271828", "161803", "141421"]


def load_dir(path: str) -> list[dict]:
    out = []
    for fn in sorted(os.listdir(path)):
        if fn.endswith(".jsonl"):
            with open(os.path.join(path, fn), encoding="utf-8") as f:
                out += [json.loads(l) for l in f if l.strip()]
    return out


def split(recs: list[dict]) -> dict:
    n = max(len(recs), 1)
    correct = sum(1 for r in recs if r["correct"])
    no_answer = sum(1 for r in recs if r["answer_extracted"] is None)
    wrong = len(recs) - correct - no_answer
    return {"n": len(recs), "correct": correct, "wrong_parseable": wrong,
            "no_parseable_answer": no_answer,
            "correct_rate": correct / n, "no_answer_rate": no_answer / n}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=os.path.join(REPO, "runs"))
    ap.add_argument("--analysis", default=os.path.join(REPO, "runs", "analysis_rung1.json"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    report: dict = {"_note": __doc__.strip(), "by_arm": {}}

    native = load_dir(os.path.join(args.runs_dir, "native"))
    nat_cells = defaultdict(list)
    for r in native:
        nat_cells[f'{r["family"]}:d{r["depth"]}'].append(r)
    report["native"] = {c: split(v) for c, v in sorted(nat_cells.items())}

    arm_dirs = sorted(d for d in os.listdir(args.runs_dir)
                      if d.startswith("randomized-")
                      and os.path.isdir(os.path.join(args.runs_dir, d)))
    arms = defaultdict(list)
    for d in arm_dirs:
        for s in SEEDS:
            if d.endswith("-s" + s):
                arms[d[len("randomized-"):-len("-s" + s)]] += load_dir(
                    os.path.join(args.runs_dir, d))

    for arm, recs in sorted(arms.items()):
        cells = defaultdict(list)
        for r in recs:
            cells[f'{r["family"]}:d{r["depth"]}'].append(r)
        block = {}
        for cell, v in sorted(cells.items()):
            touched = [r for r in v
                       if any(s.get("intervened") for s in r.get("sites", []))]
            block[cell] = {
                "all": split(v),
                "touched": split(touched),
                "untouched": split([r for r in v if r not in touched]),
            }
        report["by_arm"][arm] = block

    # 7.1(c): supplementary aggregate excluding rule 05, from independent arms
    analysis = json.load(open(args.analysis, encoding="utf-8"))
    per_rule = {a: d["pooled"]["o1_mean_penalty"]
                for a, d in analysis["arms"].items() if a != "all"}
    informative = {a: v for a, v in per_rule.items()
                   if a not in ("tier_a_03_discourse_markers",
                                "tier_a_07_list_markers")}
    ex05 = {a: v for a, v in informative.items() if a != "tier_a_05_whitespace"}
    report["supplementary_aggregate"] = {
        "frozen_aggregate_arm_o1": analysis["arms"]["all"]["pooled"]["o1_mean_penalty"],
        "per_rule_o1": per_rule,
        "mean_per_rule_o1_excluding_rule05": sum(ex05.values()) / len(ex05),
        "arms_included_in_exclusion_mean": sorted(ex05),
        "excluded_as_uninformative": ["tier_a_03_discourse_markers (0 interventions, "
                                      "structurally unavailable)",
                                      "tier_a_07_list_markers (10 interventions, "
                                      "uninformative)"],
        "_label": "MECHANISTIC DECOMPOSITION, not a replacement estimand. The "
                  "frozen Tier A aggregate O1 stands as computed.",
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    sa = report["supplementary_aggregate"]
    print(f"-> {args.out}")
    print(f"frozen aggregate O1: {sa['frozen_aggregate_arm_o1']:+.4f}")
    print(f"mean per-rule O1 excluding rule 05: "
          f"{sa['mean_per_rule_o1_excluding_rule05']:+.4f}")


if __name__ == "__main__":
    main()
