"""Audit sampler (SPEC section 8, HANDOFF item 6).

Draws ~500 intervened sites from run outputs using audit_sample_seed —
which must be committed in seeds.json BEFORE any outcome analysis — and
emits excerpt pairs in the shape judge/judge_prompt.txt expects:

- ORIGINAL and MODIFIED differ only within the marked span: MODIFIED is a
  window of the realized trace around the chosen span; ORIGINAL is the same
  window with the native span restored.
- Items are blinded: they carry only the excerpts and the span pair, in a
  seed-shuffled order. Provenance (problem, rule, run) lives in a separate
  key file that is joined back only AFTER verdicts are collected. Rule-level
  98% thresholds (frozen) are then computed per rule.
"""

from __future__ import annotations

import argparse
import json
import random

from harness.runner import load_problems  # JSONL loader, reused for runs


def sample_intervened_sites(records: list[dict], seed: int,
                            n: int = 500) -> list[tuple[dict, dict]]:
    pool = [
        (rec, s)
        for rec in records
        for s in rec.get("sites", [])
        if s.get("intervened")
    ]
    rng = random.Random(f"audit:{seed}")
    if len(pool) <= n:
        rng.shuffle(pool)
        return pool
    return rng.sample(pool, n)


def build_audit_items(pool: list[tuple[dict, dict]], seed: int,
                      context_chars: int = 150) -> tuple[list[dict], list[dict]]:
    rng = random.Random(f"audit-order:{seed}")
    order = list(range(len(pool)))
    rng.shuffle(order)

    items, key = [], []
    for audit_id, idx in enumerate(order):
        rec, site = pool[idx]
        text = rec["text"]
        start = site["start"]
        chosen = site["chosen"]
        end_in_final = start + len(chosen)
        left = text[max(0, start - context_chars):start]
        right = text[end_in_final:end_in_final + context_chars]
        items.append({
            "audit_id": audit_id,
            "original": left + site["matched"] + right,
            "modified": left + chosen + right,
            "span_before": site["matched"],
            "span_after": chosen,
        })
        key.append({
            "audit_id": audit_id,
            "problem_id": rec["id"],
            "rule_id": site["rule_id"],
            "set_id": site["set_id"],
            "site_start": start,
        })
    return items, key


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True, nargs="+",
                    help="randomized-run JSONL files")
    ap.add_argument("--seed", type=int, required=True,
                    help="audit_sample_seed from seeds.json")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--context-chars", type=int, default=150)
    ap.add_argument("--items-out", required=True)
    ap.add_argument("--key-out", required=True)
    args = ap.parse_args()

    records = [r for path in args.runs for r in load_problems(path)]
    pool = sample_intervened_sites(records, seed=args.seed, n=args.n)
    items, key = build_audit_items(pool, seed=args.seed,
                                   context_chars=args.context_chars)

    with open(args.items_out, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")
    with open(args.key_out, "w", encoding="utf-8") as f:
        for k in key:
            f.write(json.dumps(k) + "\n")
    print(f"{len(items)} audit items -> {args.items_out}; key -> {args.key_out}")


if __name__ == "__main__":
    main()
