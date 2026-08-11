"""Supplementary rung 1 re-extraction (eighth relay, unanimous 8.2(b)).

The frozen rung 1 numbers (runs/analysis_rung1.json, RESULTS.md) are PRIMARY
and untouched. This script recomputes the same estimands under the extended
extraction rule frozen for the instruct follow-on under ruling 8.1(b):

    the frozen ANSWER-line regex takes precedence; else the LAST
    \\boxed{<integer>} in the trace; nothing else accepted.

Fable's safety condition (REVIEW_LOG, eighth relay): the rule is specified
for follow-on reasons and applied to rung 1 UNMODIFIED — no rung-1-specific
tuning — and this script is committed before it is run. Sol's requirement:
extraction transition counts are published by (family, depth, arm) so
readers can see exactly where the supplementary metric differs from the
frozen one. Fable's extension: if the flips are arm-imbalanced enough to
move O1/O2 materially, that is itself a reportable measurement-sensitivity
finding; the sixth-relay non-discrimination statement extends to the
supplementary O2 automatically.

Outputs (labeled supplementary throughout):
  runs/analysis_rung1_supplementary_reextraction.json
  runs/reextraction_transitions.json
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict

from harness.analysis import analyze_arm, slope
from harness.exposure import fit_logistic, proposal_a_rows
from harness.runner import extract_answer_extended

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDS = ["271828", "161803", "141421"]


def load_dir(path: str) -> list[dict]:
    out = []
    for fn in sorted(os.listdir(path)):
        if not fn.endswith(".jsonl"):
            continue
        with open(os.path.join(path, fn), encoding="utf-8") as f:
            out += [json.loads(l) for l in f if l.strip()]
    return out


def restricted_slope(family_block: dict, depths: list[int]) -> float | None:
    pts = [(d, family_block["cells"][str(d)]["penalty"])
           for d in depths if str(d) in family_block.get("cells", {})]
    return slope(pts)


def reextract(rec: dict) -> dict:
    """Apply the extended rule to one frozen record; returns a copy with
    answer_extracted/correct recomputed and the original verdict kept for
    the transition table."""
    gen = rec["text"][rec["prompt_chars"]:]
    ext = extract_answer_extended(gen)
    new = dict(rec)
    new["extraction_rule"] = "extended"
    new["answer_extracted"] = ext
    new["correct"] = (ext is not None
                      and ext == str(rec["answer_expected"]))
    new["_frozen_correct"] = bool(rec["correct"])
    return new


def tally_transitions(records: list[dict], arm: str,
                      table: dict) -> None:
    for r in records:
        key = (arm, str(r["family"]), int(r["depth"]))
        row = table.setdefault(key, {
            "records": 0, "flips_to_correct": 0, "flips_to_wrong": 0})
        row["records"] += 1
        if r["correct"] and not r["_frozen_correct"]:
            row["flips_to_correct"] += 1
        elif r["_frozen_correct"] and not r["correct"]:
            row["flips_to_wrong"] += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=os.path.join(REPO, "runs"))
    ap.add_argument("--out-analysis", default=os.path.join(
        REPO, "runs", "analysis_rung1_supplementary_reextraction.json"))
    ap.add_argument("--out-transitions", default=os.path.join(
        REPO, "runs", "reextraction_transitions.json"))
    args = ap.parse_args()

    runs = args.runs_dir
    transitions: dict = {}

    native = [reextract(r) for r in load_dir(os.path.join(runs, "native"))]
    tally_transitions(native, "native", transitions)

    exposure = {}
    with open(os.path.join(runs, "native-exposure.jsonl"), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                exposure[e["id"]] = e["native_eligible_total"]

    arm_dirs = sorted(d for d in os.listdir(runs)
                      if d.startswith("randomized-")
                      and os.path.isdir(os.path.join(runs, d)))
    arms = defaultdict(dict)          # arm label -> seed -> records
    for d in arm_dirs:
        for s in SEEDS:
            if d.endswith("-s" + s):
                recs = [reextract(r)
                        for r in load_dir(os.path.join(runs, d))]
                arms[d[len("randomized-"):-len("-s" + s)]][s] = recs
                tally_transitions(recs, d[len("randomized-"):-len("-s" + s)],
                                  transitions)

    results: dict = {
        "_status": "SUPPLEMENTARY (eighth relay 8.2(b), unanimous). The "
                   "frozen rung 1 numbers in runs/analysis_rung1.json remain "
                   "the primary preregistered result. This file recomputes "
                   "the same estimands under the extended extraction rule "
                   "frozen for the instruct follow-on (8.1(b)), applied to "
                   "rung 1 unmodified, so base and follow-on share one "
                   "measurement rule. The sixth-relay non-discrimination "
                   "pre-declaration extends to this O2.",
        "arms": {},
    }

    for arm, by_seed in sorted(arms.items()):
        arm_out: dict = {"per_seed": {}, "pooled": None}
        pooled_records = []
        for s in SEEDS:
            recs = by_seed.get(s)
            if not recs:
                continue
            pooled_records += recs
            res = analyze_arm(native, recs)
            for fam, blk in res["families"].items():
                if fam == "reachability":
                    blk["o2_slope_d4_to_d8"] = restricted_slope(blk, [4, 6, 8])
            arm_out["per_seed"][s] = res

        pooled = analyze_arm(native * len(by_seed), pooled_records)
        for fam, blk in pooled["families"].items():
            if fam == "reachability":
                blk["o2_slope_d4_to_d8"] = restricted_slope(blk, [4, 6, 8])
        arm_out["pooled"] = pooled

        # Proposal A under the supplementary extractor (reachability grid,
        # pooled across seeds) — same design matrix, re-extracted outcomes.
        total_iv = sum(1 for r in pooled_records
                       for st in r.get("sites", []) if st.get("intervened"))
        reach_rand = [r for r in pooled_records if r["family"] == "reachability"]
        reach_nat = [r for r in native if r["family"] == "reachability"]
        if reach_rand and total_iv > 0:
            xs, ys = proposal_a_rows(reach_rand, reach_nat * len(by_seed),
                                     exposure)
            beta = fit_logistic(xs, ys)
            arm_out["proposal_a"] = {
                "terms": ["intercept", "arm", "depth", "native_count",
                          "arm:native_count", "arm:depth"],
                "coefficients": beta,
                "arm_x_depth": beta[5],
                "n_rows": len(xs),
            }
        else:
            arm_out["proposal_a"] = {
                "status": "not computed — zero interventions in this arm "
                          "(structurally unavailable, not a null effect)"}

        results["arms"][arm] = arm_out

    with open(args.out_analysis, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    trans_rows = [
        {"arm": a, "family": fam, "depth": d, **row}
        for (a, fam, d), row in sorted(transitions.items())
    ]
    trans_out = {
        "_status": "Extraction transition counts, frozen -> extended rule "
                   "(eighth relay 8.2(b); published per Sol's requirement). "
                   "A row per (arm, family, depth); zero-flip rows included "
                   "so readers see where the metrics coincide.",
        "rows": trans_rows,
        "totals": {
            "records": sum(r["records"] for r in trans_rows),
            "flips_to_correct": sum(r["flips_to_correct"] for r in trans_rows),
            "flips_to_wrong": sum(r["flips_to_wrong"] for r in trans_rows),
        },
    }
    with open(args.out_transitions, "w", encoding="utf-8") as f:
        json.dump(trans_out, f, indent=2)

    # Console comparison against the frozen primary, when present.
    frozen_path = os.path.join(runs, "analysis_rung1.json")
    frozen = None
    if os.path.exists(frozen_path):
        with open(frozen_path, encoding="utf-8") as f:
            frozen = json.load(f)

    print(f"supplementary analysis -> {args.out_analysis}")
    print(f"transition counts      -> {args.out_transitions}")
    print(f"total flips: +{trans_out['totals']['flips_to_correct']} correct, "
          f"-{trans_out['totals']['flips_to_wrong']} wrong, "
          f"{trans_out['totals']['records']} records")
    for arm, a in sorted(results["arms"].items()):
        p = a["pooled"]
        reach = p["families"].get("reachability", {})
        line = (f"{arm}: O1 {p['o1_mean_penalty']:+.4f}"
                f"  O2reach {reach.get('o2_slope')}"
                f"  d4-d8 {reach.get('o2_slope_d4_to_d8')}")
        if frozen and arm in frozen.get("arms", {}):
            fp = frozen["arms"][arm]["pooled"]
            line += f"   (frozen O1 {fp['o1_mean_penalty']:+.4f})"
        print(line)


if __name__ == "__main__":
    main()
