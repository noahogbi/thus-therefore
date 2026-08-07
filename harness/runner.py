"""Run harness (HANDOFF item: main run, native vs. neutral-randomized).

Runs problems (JSONL from tasks/generate_tasks.py) through the decoder in
one of two modes:

- native      — pure greedy, no site machinery (control arm)
- randomized  — greedy + neutral-choice randomization per SPEC section 2

`rules` selects a per-rule arm (only those rules are randomized/logged);
None randomizes all Tier A rules together. Per-rule observables (SPEC
section 2 registers O1/O2 separately per rule) require per-rule arms — the
arm plan is decided before the GPU run, not here.

Seeding: each problem gets its own deterministic rng derived from
(intervention_sampling_seed, problem id), so runs are reproducible per
problem and resumable/parallelizable without order effects.

Every record carries the full realized text, the site log, density, and
answer correctness. Written as JSONL; the git-committed seed +
FREEZE_MANIFEST make the whole run reproducible.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Iterable, Iterator

from harness.decoder import InterventionDecoder
from harness.scoring import EligibilityScorer, SequenceLM

_ANSWER_RE = re.compile(r"ANSWER:\s*(-?\d+|none)", re.IGNORECASE)


def extract_answer(text: str) -> str | None:
    """Last 'ANSWER: <int|none>' in the trace, numerically normalized."""
    matches = _ANSWER_RE.findall(text)
    if not matches:
        return None
    raw = matches[-1]
    if raw.lower() == "none":
        return "none"
    return str(int(raw))


def _problem_rng(seed: int, problem_id: str) -> random.Random:
    return random.Random(f"{seed}:{problem_id}")


def run_problems(lm: SequenceLM, problems: Iterable[dict], mode: str,
                 seed: int, rules: set[str] | None = None,
                 max_new_tokens: int = 1024,
                 lookahead_chars: int = 100) -> Iterator[dict]:
    if mode not in ("native", "randomized"):
        raise ValueError(f"unknown mode: {mode}")
    scorer = EligibilityScorer(lm)
    for prob in problems:
        decoder = InterventionDecoder(
            lm=lm, scorer=scorer,
            rng=_problem_rng(seed, prob["id"]),
            lookahead_chars=lookahead_chars,
            intervene=(mode == "randomized"),
            rules=rules,
        )
        result = decoder.generate(prob["prompt"], max_new_tokens=max_new_tokens)
        extracted = extract_answer(result.text[len(prob["prompt"]):])
        yield {
            "id": prob["id"],
            "family": prob.get("family"),
            "depth": prob.get("depth"),
            "mode": mode,
            "rules_arm": sorted(rules) if rules else "all",
            "seed": seed,
            "text": result.text,
            "prompt_chars": result.prompt_chars,
            "generated_tokens": result.generated_tokens,
            "ended": result.ended,
            "answer_expected": prob.get("answer"),
            "answer_extracted": extracted,
            "correct": (extracted is not None
                        and extracted == str(prob.get("answer"))),
            "sites": [s.to_dict() for s in result.sites],
            "density": result.density,
        }


def load_problems(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--revision", default=None)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--problems", required=True)
    ap.add_argument("--mode", choices=["native", "randomized"], required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--rules", default=None,
                    help="comma-separated rule_ids for a per-rule arm")
    ap.add_argument("--max-new-tokens", type=int, default=1024)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from harness.scoring import HFCausalLM
    lm = HFCausalLM(args.model_id, revision=args.revision,
                    device=args.device, dtype=args.dtype)
    rules = set(args.rules.split(",")) if args.rules else None
    problems = load_problems(args.problems)

    with open(args.out, "w", encoding="utf-8") as f:
        for i, record in enumerate(run_problems(
                lm, problems, mode=args.mode, seed=args.seed, rules=rules,
                max_new_tokens=args.max_new_tokens)):
            f.write(json.dumps(record) + "\n")
            f.flush()
            print(f"[{i + 1}/{len(problems)}] {record['id']} "
                  f"correct={record['correct']} sites={len(record['sites'])}")


if __name__ == "__main__":
    main()
