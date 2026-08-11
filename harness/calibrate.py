"""Depth calibrator (SPEC section 7, HANDOFF item 5).

Required serial depth is calibrated per (family, depth) by the with-trace
vs. without-trace accuracy gap, under NATIVE GREEDY decoding only — no
interventions here. The main comparison later uses the (family, depth) cells
where the gap is large (tasks the model solves with CoT and fails without).

Implementation note (harness, not frozen content): the without-trace
condition appends NO_TRACE_SUFFIX to the frozen generator's prompt,
instructing an immediate answer. The frozen prompt text itself is unchanged;
the suffix is fixed here so both calibration arms are reproducible.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from typing import Iterable

from harness.runner import load_problems, run_problems
from harness.scoring import SequenceLM

NO_TRACE_SUFFIX = (
    "\n\nDo not show any reasoning. Respond immediately with only the final "
    "answer line.\n"
)


def calibrate(lm: SequenceLM, problems: Iterable[dict],
              max_new_tokens: int = 1024,
              no_trace_max_new_tokens: int = 32,
              extended_extraction: bool = False) -> dict:
    problems = list(problems)
    no_trace = [
        {**p, "id": p["id"] + ":notrace", "prompt": p["prompt"] + NO_TRACE_SUFFIX}
        for p in problems
    ]

    cells: dict[tuple, dict] = defaultdict(
        lambda: {"with": [], "without": []})
    for rec in run_problems(lm, problems, mode="native", seed=0,
                            max_new_tokens=max_new_tokens,
                            extended_extraction=extended_extraction):
        cells[(rec["family"], rec["depth"])]["with"].append(rec["correct"])
    for rec in run_problems(lm, no_trace, mode="native", seed=0,
                            max_new_tokens=no_trace_max_new_tokens,
                            extended_extraction=extended_extraction):
        cells[(rec["family"], rec["depth"])]["without"].append(rec["correct"])

    grid = {}
    for key, v in cells.items():
        w = sum(v["with"]) / len(v["with"]) if v["with"] else None
        wo = sum(v["without"]) / len(v["without"]) if v["without"] else None
        grid[key] = {
            "with_trace_acc": w,
            "without_trace_acc": wo,
            "gap": (w - wo) if (w is not None and wo is not None) else None,
            "n": len(v["with"]),
        }
    return grid


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--revision", default=None)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--problems", required=True, nargs="+")
    ap.add_argument("--max-new-tokens", type=int, default=1024)
    ap.add_argument("--extended-extraction", action="store_true")
    ap.add_argument("--extra-terminal-token", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from harness.scoring import HFCausalLM
    lm = HFCausalLM(args.model_id, revision=args.revision,
                    device=args.device, dtype=args.dtype,
                    extra_terminal_tokens=(args.extra_terminal_token or None))
    problems = [p for path in args.problems for p in load_problems(path)]
    grid = calibrate(lm, problems, max_new_tokens=args.max_new_tokens,
                     extended_extraction=args.extended_extraction)

    serializable = {f"{fam}:{depth}": cell for (fam, depth), cell in grid.items()}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)
    for key, cell in sorted(serializable.items()):
        print(key, cell)


if __name__ == "__main__":
    main()
