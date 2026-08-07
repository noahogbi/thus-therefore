"""O1/O2 analysis (SPEC sections 6 and 9, HANDOFF item 7).

Per arm (a per-rule randomization arm, or the all-rules aggregate arm):

- O1: raw accuracy penalty (native accuracy minus randomized accuracy),
  per (family, depth) cell and as an unweighted mean over cells.
- O2: depth interaction — the least-squares slope of the penalty against
  depth, per family. "Positive" = penalty increases with depth.

Frozen reporting policy (CLAUDE.md): O1 and O2 are reported separately, per
rule and aggregate. DISPUTED CELLS ARE SEPARATE ARMS AND ARE NEVER
AGGREGATED — this module analyzes one arm at a time and never pools arms;
there is deliberately no cross-arm combination function here.

The harness is outcome-neutral: nothing here knows which sign either party
registered.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict


def slope(points: list[tuple[float, float]]) -> float | None:
    """Least-squares slope of y on x; None if underdetermined."""
    xs = {x for x, _ in points}
    if len(points) < 2 or len(xs) < 2:
        return None
    n = len(points)
    mx = sum(x for x, _ in points) / n
    my = sum(y for _, y in points) / n
    num = sum((x - mx) * (y - my) for x, y in points)
    den = sum((x - mx) ** 2 for x, _ in points)
    return num / den


def _acc_by_cell(records: list[dict]) -> dict[tuple, list[bool]]:
    cells: dict[tuple, list[bool]] = defaultdict(list)
    for r in records:
        cells[(r["family"], r["depth"])].append(bool(r["correct"]))
    return cells


def analyze_arm(native: list[dict], randomized: list[dict]) -> dict:
    nat = _acc_by_cell(native)
    rnd = _acc_by_cell(randomized)

    families: dict[str, dict] = defaultdict(lambda: {"cells": {}})
    unmatched = []
    penalties = []
    for key in sorted(rnd, key=lambda k: (str(k[0]), k[1])):
        family, depth = key
        if key not in nat:
            unmatched.append(f"{family}:{depth}")
            continue
        acc_n = sum(nat[key]) / len(nat[key])
        acc_r = sum(rnd[key]) / len(rnd[key])
        penalty = acc_n - acc_r
        penalties.append(penalty)
        families[family]["cells"][str(depth)] = {
            "native_acc": acc_n,
            "randomized_acc": acc_r,
            "penalty": penalty,
            "n_native": len(nat[key]),
            "n_randomized": len(rnd[key]),
        }

    for family, data in families.items():
        pts = [(int(d), c["penalty"]) for d, c in data["cells"].items()]
        data["o2_slope"] = slope(pts)

    return {
        "families": dict(families),
        "o1_mean_penalty": (sum(penalties) / len(penalties)) if penalties else None,
        "unmatched_cells": unmatched,
    }


def main() -> None:
    from harness.runner import load_problems

    ap = argparse.ArgumentParser()
    ap.add_argument("--native", required=True, nargs="+")
    ap.add_argument("--randomized", required=True, nargs="+")
    ap.add_argument("--arm-label", required=True,
                    help="e.g. tier_a_01_connectives, tier_a_all")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    native = [r for p in args.native for r in load_problems(p)]
    randomized = [r for p in args.randomized for r in load_problems(p)]
    result = {"arm": args.arm_label, **analyze_arm(native, randomized)}

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
