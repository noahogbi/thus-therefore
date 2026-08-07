# HANDOFF — Read This First (Claude Code)

You are implementing a pre-registered experiment whose design is FROZEN. Your job is
engineering fidelity, not design improvement.

## Authority order

1. **SPEC.md** — normative. If code and SPEC conflict, SPEC wins.
2. **FREEZE.md** — process rules (hashing, validation, amendment protocol).
3. **rules/** — the frozen candidate tables. Implement them exactly; where a table's
   contextual rule is ambiguous, the resolution is CONSERVATIVE: skip the site.
   Skipping sites lowers density (reported, harmless); wrongly randomizing a
   non-neutral site contaminates the run.
4. `transcript.md` (if Noah adds it) — background only. NOT normative. Do not mine it
   for design changes; anything that mattered was moved into SPEC.md.

## What is frozen (do not modify without triggering FREEZE.md amendment protocol)

SPEC.md, FREEZE.md, rules/tier_a/*.json, judge/judge_prompt.txt,
tasks/generate_tasks.py, Delta = 1.5, the five-property validation criteria, the
98% rule-level threshold, the prefix-eligibility wording in SPEC section 2.

## What you are building (harness/ — currently empty by design)

1. **Site matcher** — applies rules/tier_a/*.json to a growing token sequence.
   Tokenizer-deterministic, no model calls. Must handle span-level sites (candidates
   may differ in token count). Overlap resolution: lowest rule_id wins.
2. **Eligibility scorer** — for each matched site, force-score every candidate span
   under the frozen model given the realized prefix (including all prior
   interventions), per SPEC section 2. Candidate eligible iff within 1.5 nats of the
   best candidate. >= 2 eligible candidates required, else skip.
3. **Intervention decoder** — greedy everywhere; at eligible sites, uniform sample
   among eligible candidates, splice the span, recompute KV from the realized
   sequence (an exact-prefix rebuild is a bit-identity sanity check, not a
   condition). Log every site: rule_id, candidates, chosen, position.
4. **Density logger** — eligible sites per 1,000 generated tokens, per rule, per run.
5. **Depth calibrator** — with-trace vs. without-trace accuracy per (family, depth)
   to establish the calibrated serial-depth axis before the main comparison.
6. **Audit sampler** — draw ~500 logged sites using audit_sample_seed (committed
   BEFORE outcome analysis), emit excerpt pairs formatted for judge/judge_prompt.txt,
   blind the condition labels.
7. **Analysis** — per rule and Tier A aggregate: O1 (raw penalty) and O2 (depth
   interaction), reported separately. Disputed cells (rules/disputed/) are separate
   arms, never aggregated — they are follow-on work, not part of the first run.

## Build order and checkpoints with Noah

1. Fill environment.json (model, tokenizer, decoding impl, judge — pin revisions).
2. Implement matcher + scorer; run matcher-only over sample traces; review site
   matches with Noah BEFORE any intervention run (cheap sanity pass).
3. Fill seeds.json; run scripts/hash_commit.py; publish manifest_hash.
4. Depth calibration pass (native greedy only) — pick the (family, depth) grid where
   with/without-trace gaps are large.
5. Main run: native vs. neutral-randomized, across the calibrated depth grid,
   multiple intervention seeds.
6. Audit, then analysis. If any rule fails audit: remove rule, new manifest, rerun.

## Hardware notes

Target: rented RTX 4090 (24GB) — Vast.ai / RunPod. Models: Qwen2.5-7B/14B-class or
R1-distill for the base/light-instruct condition; OLMo 2 / Tülu 3 staged checkpoints
(SFT / DPO / RLVR) for the training-history axis later. HF transformers or vLLM with
a logits-processor/forced-scoring path; Ollama is not usable (no per-step logit
access). Judge calls are post-hoc only — never in the decoding loop.

## Registered predictions (context for analysis output, not something to optimize)

- Sol: positive depth interaction on the Tier A aggregate.
- Fable: ~zero depth interaction on base/light-instruct for every rule; positive
  emerging only on outcome-filtered checkpoints, concentrated in high-density,
  high-entropy rules (connectives, discourse markers first).

The harness must be equally capable of producing either result. Nature decides who
pays.
