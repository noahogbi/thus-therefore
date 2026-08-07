# CLAUDE.md — Standing Instructions for This Repo

You are implementing a pre-registered, frozen experiment. Your job is engineering
fidelity, not design improvement. Read HANDOFF.md for the build plan and SPEC.md for
the design. This file governs how you work here, every session.

## Authority order

SPEC.md > FREEZE.md > rules/*.json > HANDOFF.md > this file > anything else.
`transcript.md`, if present, is background only — never mine it for design changes.
If code and SPEC conflict, the code is wrong.

## Non-negotiable working rules

1. **Never modify frozen artifacts.** SPEC.md, FREEZE.md, rules/tier_a/*.json,
   judge/judge_prompt.txt, tasks/generate_tasks.py, Δ = 1.5, the validation criteria.
   If Noah asks for a change to any of these, remind him it triggers the FREEZE.md
   amendment protocol (new pre-registration, new manifest, fresh run) and get
   explicit confirmation before touching anything.

2. **Ambiguity resolves conservatively: skip the site.** When a rule's contextual
   matcher is ambiguous about whether a location qualifies, do not randomize it.
   Skipped sites lower density, which is reported and harmless. A wrongly randomized
   non-neutral site contaminates the run. Never "fix" ambiguity by broadening a rule.

3. **No design improvements.** You will notice things that look improvable — a
   cleaner equivalence class, a better rule, a smarter sampler. Log them in
   IDEAS_FOR_NEXT_PREREGISTRATION.md and move on. The freeze exists precisely
   because post-hoc design adjustment is the failure mode this experiment guards
   against.

4. **Judge calls are post-hoc only.** Never in the decoding loop. Never during
   generation. The intervention must be fully mechanical.

5. **The harness must be outcome-neutral.** Both registered predictions (SPEC §6)
   must be equally producible by your code. Never special-case, tune, or debug
   toward either expected result. If a result looks wrong, suspect the harness, and
   verify with the bit-identity sanity check (exact-prefix KV rebuild) before
   suspecting the science.

## MANDATORY CHECKPOINT — before hash_commit.py is ever run

This gate was insisted on by Fable, the model that drafted the rule tables, for
exactly that reason: the tables are where its judgment could have leaked, and per
FREEZE.md a hashed rule can only be removed whole, never patched. Do not let Noah
skip this, and do not skip it yourself.

**Step 1 — Matcher-only dry run.** Implement the site matcher first, before any
scorer or decoder. Run it over 20+ diverse sample traces (generate them with any
model, or hand-write them: math reasoning, graph reasoning, prose-heavy reasoning,
traces containing code blocks, quotes, negative numbers, ranges like 5-10,
"so that" clauses, conditional "then", ordinal enumerations, possessive "its").

**Step 2 — Adversarial review with Noah.** Present every matched site in context,
grouped by rule, and walk Noah through them with this explicit framing: *find the
site that should not have matched.* Specifically hunt for:
   - "so" matched in comparative/purpose constructions the exclusions missed
   - "Then" carrying conditional (if-then) meaning — that is dependency structure
   - a minus sign the matcher called binary that could parse as unary or a range
   - contraction sites inside quoted text or possessive "its"
   - whitespace sites that would merge or split steps (granularity is protected)
   - any candidate substitution that adds/removes hedging or changes what is
     explicit — channel 2 leakage
   - discourse-marker swaps that break an enumeration pattern elsewhere in trace

**Step 3 — Disposition.** For each bad match: if an existing exclusion was
misimplemented, fix the matcher code (code is not frozen; tables are). If the TABLE
itself is wrong, the table must be amended BEFORE the freeze — this is the only
window in which tables can change without triggering a rerun, because nothing has
been hashed yet. Record every table change in a REVIEW_LOG.md with the reason.

**Step 4 — Sign-off.** Only after Noah explicitly signs off on the reviewed site
list: fill seeds.json and environment.json, run scripts/hash_commit.py, and have
Noah publish the manifest_hash somewhere timestamped (git commit + push is fine).
From that moment the amendment protocol applies to everything.

## Environment pinning (before the checkpoint's Step 4)

environment.json must pin: model id + revision hash, tokenizer id + revision hash,
decoding implementation + version, judge model + revision. Model version alone is
insufficient — the experiment is tokenizer-level. Sol required this; honor it.

## Session hygiene

- Start each session by reading README.md status boxes; update them as work lands.
- Commit small and often; the git history is part of the experiment's audit trail.
- GPU work (eligibility scoring, generation) targets a rented RTX 4090 via SSH;
  keep everything runnable headless with a single entry script per phase.
- Analysis reports O1 (raw penalty) and O2 (depth interaction) separately, per rule
  and aggregate; disputed cells never enter aggregates. This is frozen reporting
  policy, not a style choice.
