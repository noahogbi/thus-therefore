"""Matcher-only dry run (CLAUDE.md checkpoint, Step 1).

Runs the site matcher over every trace in samples/traces/ and writes
REVIEW_SITES.md: every matched site shown in context, grouped by rule, framed
for the adversarial review in Step 2. No model calls, no interventions.

Usage:
    python harness/run_matcher.py [--out REVIEW_SITES.md]
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from harness.matcher import match_sites

REPO = Path(__file__).resolve().parent.parent
TRACES = REPO / "samples" / "traces"

CONTEXT_CHARS = 90


def show(s: str) -> str:
    return s.replace("\n", "\\n")


def excerpt(text: str, start: int, end: int) -> str:
    a = max(0, start - CONTEXT_CHARS)
    b = min(len(text), end + CONTEXT_CHARS)
    pre = ("…" if a > 0 else "") + text[a:start]
    post = text[end:b] + ("…" if b < len(text) else "")
    return f"{show(pre)}⟦{show(text[start:end])}⟧{show(post)}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "REVIEW_SITES.md"))
    args = ap.parse_args()

    by_rule: dict[str, list] = defaultdict(list)
    trace_count, token_est = 0, 0
    for path in sorted(TRACES.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        trace_count += 1
        token_est += len(text.split())
        for site in match_sites(text):
            by_rule[site.rule_id].append((path.name, text, site))

    total = sum(len(v) for v in by_rule.values())
    lines = [
        "# Matcher dry-run — adversarial review sheet",
        "",
        "**Task for the reviewer: find the site that should NOT have matched.**",
        "",
        f"{total} sites across {trace_count} traces (~{token_est} words). Every",
        "matched span is shown as ⟦span⟧ with surrounding context. For each site",
        "ask: would swapping the span for any listed candidate change ANY of —",
        "propositions, dependency structure, hedging, which intermediates are",
        "explicit, step granularity/schedule? If yes for even one candidate, the",
        "site is bad and must be dispositioned (matcher fix vs. table amendment)",
        "per CLAUDE.md Step 3.",
        "",
    ]

    for rule_id in sorted(by_rule):
        sites = by_rule[rule_id]
        lines.append(f"## {rule_id} — {len(sites)} sites")
        lines.append("")
        for i, (name, text, s) in enumerate(sites, 1):
            cands = " | ".join(show(c) for c in s.candidates)
            lines.append(f"**{rule_id[:9]}#{i}** `{name}` [{s.start}:{s.end}] set `{s.set_id}`")
            lines.append(f"  candidates: `{cands}`")
            lines.append(f"> {excerpt(text, s.start, s.end)}")
            lines.append("")

    lines.append("## Rules with zero sites in this corpus")
    lines.append("")
    all_rules = {f"tier_a_0{i}" for i in range(1, 8)}
    hit = {r[:9] for r in by_rule}
    for r in sorted(all_rules - hit):
        lines.append(f"- {r} — no sites matched; needs targeted traces or is expected-low-density")
    if not (all_rules - hit):
        lines.append("- none — every rule produced at least one site")

    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{total} sites from {trace_count} traces -> {args.out}")
    for rule_id in sorted(by_rule):
        print(f"  {rule_id}: {len(by_rule[rule_id])}")


if __name__ == "__main__":
    main()
