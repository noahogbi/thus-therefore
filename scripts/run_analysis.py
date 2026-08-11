"""Compute the full rung 1 analysis exactly as ruled (sixth relay, 6b).

Registered, primary:
  O1 — raw accuracy penalty (native minus randomized) per (family, depth)
       cell, per arm, per intervention seed and pooled across seeds.
  O2 — least-squares slope of penalty against depth, per family; the
       reachability d4->d8 restricted slope is reported separately because
       the third consultation designated it the primary read.

Supplementary, adopted:
  S1 — realized exposure (scripts/s1_exposure_report.py).
  Proposal A — trace-level logistic model
       correct ~ arm + depth + native_count + arm*native_count + arm*depth
  fit within the calibrated reachability grid, per arm.

Both parties pre-declared (blind) that this run's O2 is non-discriminating
between their registered predictions. Nothing here selects cells or
estimands on measured exposure.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict

from harness.analysis import analyze_arm, slope
from harness.exposure import fit_logistic, proposal_a_rows

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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", default=os.path.join(REPO, "runs"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    runs = args.runs_dir
    native = load_dir(os.path.join(runs, "native"))

    exposure = {}
    exp_path = os.path.join(runs, "native-exposure.jsonl")
    with open(exp_path, encoding="utf-8") as f:
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
                arms[d[len("randomized-"):-len("-s" + s)]][s] = load_dir(
                    os.path.join(runs, d))

    results: dict = {
        "_ruling": "sixth relay 6b (unanimous): O1/O2 published as registered; "
                   "both parties pre-declared this run's O2 non-discriminating "
                   "between their depth-interaction predictions.",
        "arms": {},
    }

    for arm, by_seed in sorted(arms.items()):
        arm_out: dict = {"per_seed": {}, "pooled": None,
                         "interventions_by_seed": {}}
        pooled_records = []
        for s in SEEDS:
            recs = by_seed.get(s)
            if not recs:
                continue
            pooled_records += recs
            arm_out["interventions_by_seed"][s] = sum(
                1 for r in recs for st in r.get("sites", []) if st.get("intervened"))
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
        arm_out["total_interventions"] = sum(arm_out["interventions_by_seed"].values())

        # Proposal A: reachability grid only, pooled across seeds
        reach_rand = [r for r in pooled_records if r["family"] == "reachability"]
        reach_nat = [r for r in native if r["family"] == "reachability"]
        if reach_rand and arm_out["total_interventions"] > 0:
            xs, ys = proposal_a_rows(reach_rand, reach_nat * len(by_seed), exposure)
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

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"analysis -> {args.out}")
    for arm, a in sorted(results["arms"].items()):
        p = a["pooled"]
        reach = p["families"].get("reachability", {})
        print(f"\n{arm}  (interventions: {a['total_interventions']})")
        print(f"  O1 mean penalty (pooled): {p['o1_mean_penalty']}")
        print(f"  O2 reachability slope   : {reach.get('o2_slope')}")
        print(f"  O2 reachability d4->d8  : {reach.get('o2_slope_d4_to_d8')}")


if __name__ == "__main__":
    main()
