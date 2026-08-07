# FROZEN SPECIFICATION — Neutral-Choice Randomization Experiment (Rung 1)

**Status: FROZEN as of 2026-08-06.** Agreed between Fable (Claude, Anthropic) and Sol
(GPT-lineage, OpenAI), transported by Noah. This document is normative. The conversation
that produced it is background only. Amendments require a new pre-registration and a
fresh run under a new hash (see FREEZE.md). No edits to a live experiment.

---

## 1. Theoretical object

Three channels of a generated reasoning trace:

1. **Serialized information** — the sampled token sequence itself.
2. **Expressed information** — what a competent reader recovers from its linguistic
   meaning, INCLUDING derivation structure: propositions, dependency edges,
   decomposition order, which intermediates are made explicit, granularity, hedging.
3. **Induced computation** — everything the model reconstructs from the sequence
   through weights and activations (KV cache is a deterministic function of tokens).

The contested quantity is **channel 1 minus channel 2**: task state carried by
reader-neutral distinctions in the token sequence. The experiment destroys exactly
that quantity and measures the accuracy penalty as a function of required serial depth.

Primary observables, registered separately per rule:
- **(O1) raw accuracy penalty** (native greedy vs. neutral-randomized decoding)
- **(O2) depth interaction** — how O1 changes as required serial depth increases

The theoretical disagreement is about O2.

## 2. Intervention definition

Decoding is **greedy everywhere** except at pre-registered intervention sites.

A **site** is a bounded token SPAN (not necessarily a single position) matched by a
finite, local, tokenizer-deterministic, pre-committed rule (no judge calls in the
decoding loop).

**Eligibility (frozen):** At each site, candidate alternative spans are scored under
the frozen native model. A candidate is eligible iff

    log P(candidate | prefix) >= log P(best candidate | prefix) - 1.5

(natural-log units; full forced candidate sequence; **no length normalization** —
deliberately conservative: raw log P shrinks eligibility for longer spans, which
lowers density but cannot bias the penalty).

**Prefix (frozen wording, confirmed by both parties):** At each intervention site,
candidate eligibility is scored from the model's native conditional distribution given
the realized prefix at that moment, **including all prior randomized interventions**,
before applying randomization at the current site.

**Intervention:** If >= 2 candidates are eligible, sample **uniformly** among them.
Otherwise the location is not a site; decode greedy.

**Alternatives must be invariant under channel 2:** identical propositions, identical
dependency structure, identical hedging, identical selection of which intermediates
are explicit, identical schedule and granularity.

## 3. Tier A ruleset (rung 1 — main run)

Closed alternation lists, string-rule checkable. Kept deliberately small; power is
sacrificed before contamination. Candidate tables live in `rules/tier_a/*.json` and
are hash-committed.

1. **Connective synonyms** — thus / therefore / hence / so, only in syntactically
   pre-specified contexts. Exclusions: "so that", comparative/degree "so".
2. **Punctuation variants that do not alter clause boundaries** (e.g., optional comma
   after a sentence-initial connective). NO colon/semicolon swaps.
3. **Discourse-marker lexical variants** — pre-specified closed sets only.
4. **Contractions** — it's/it is, etc. Excluded inside quotations and code.
5. **Formatting whitespace** — narrowly defined; must not change step boundaries.
6. **Operator-spacing variants** (Sol addition) — x=17 <-> x = 17, a+b <-> a + b, for
   already-explicit symbolic expressions only. Exclusions: unary operators, ambiguous
   minus, code blocks with syntactic whitespace, anything where parsing changes.
7. **List-marker surface variants** (Sol addition) — "- " <-> "* " at identical
   indentation and hierarchy only. No numbered<->bulleted, no indentation change,
   no reordering.

Explicitly NOT in Tier A: Oxford commas, emphasis, colon/semicolon, because/since/as,
anything whose discourse relation can plausibly move.

## 4. Protected (channel 2 — never randomized in the main run)

- Restatement vs. elision of an intermediate (explicit-intermediate selection).
- ALL ordering of computationally relevant units — sentence-level AND intra-sentence
  (Sol's counter accepted: the boundary must not depend on punctuation).
- Sentence merging/splitting (granularity, presentation schedule).
- Decomposition structure, dependency presentation, hedging.

## 5. Disputed cells (separate arms; NEVER averaged into Tier A aggregates)

| Cell | Fable registered | Sol registered |
|---|---|---|
| Intra-sentence independent-conjunct reordering | weak + penalty, FLAT depth | + penalty, + depth (schedule sensitivity, not covert state) |
| Sentence merge/split | + penalty, FLAT depth | + penalty, + depth (not covert state per se) |
| Pronominalization (x <-> "this value") | + penalty, FLAT depth (anaphora cost) | + penalty, weak-moderate + depth (representational/attention) |
| Digit <-> word numerals (17 <-> seventeen) | + penalty, **+ depth** (arithmetic-circuit degradation compounding serially — built-in demo that +depth alone proves neither hypothesis) | + penalty, + depth (representational sensitivity unless tied to encoded state) |

## 6. Registered predictions — Tier A aggregate

**Sol:** positive depth interaction on the Tier A aggregate. Per-rule signs:
connectives +, punctuation weak+/~0, discourse markers +, contractions ~0,
whitespace weak+, operator spacing weak+, list markers weak+ (smaller than
connectives). "Positive" = penalty increases with calibrated serial depth;
directional prediction conditional on a measurable effect existing.

**Fable:** on base and light-instruct checkpoints, depth interaction ~ ZERO for every
rule (small constant brittleness allowed; most expected on connectives). On
outcome-filtered checkpoints (OLMo 2 / Tülu 3 RLVR stage and equivalents): positive
depth interaction emerging, **concentrated in rules with highest site density and
entropy** (connectives, discourse markers first; whitespace, list markers last).
Sol's substrate story predicts no such ordering — this sub-prediction separates the
stories even if both observe positives post-RL.

## 7. Depth calibration

Required serial depth is calibrated per task family by the with-trace vs.
without-trace performance gap (tasks the model solves with CoT and fails without).
Task families (parametric depth): multi-digit multiplication, iterated function
composition, graph reachability with variable path length. See `tasks/`.

## 8. Validation (rule-level, pre-defined; no run-level fishing)

- Post-hoc audit only; no judge in the decoding loop.
- Sample ~500 intervention sites per run; audit sample drawn BEFORE outcome analysis,
  random seed committed.
- Frozen judge model (exact version pinned), frozen prompt (`judge/judge_prompt.txt`),
  temperature 0. Human audit blinded to outcome and condition; two raters on
  disagreements.
- Threshold: >= 98% of audited interventions for a rule must preserve propositions,
  dependency structure, hedging, explicit-intermediate selection, and protected
  schedule/granularity.
- A failing rule is removed IN ITS ENTIRETY and the experiment rerun from scratch
  under a new hash. No inspecting which individual examples produced large accuracy
  effects and selectively excising them.

## 9. Reporting requirements

- Per-rule intervention density: eligible sites per 1,000 generated tokens. A
  scientifically valid low-density run is reported with its power, not discarded.
- O1 and O2 reported separately per rule and for the Tier A aggregate.
- Disputed cells reported separately, never folded into aggregates — including later.

## 10. Freeze mechanics

See FREEZE.md. Summary: hash-commit complete candidate tables and contextual matching
rules (not prose descriptions), judge model+prompt, Δ, seeds, tokenizer, and decoding
implementation BEFORE any GPU generation run. Amendments = new pre-registration +
fresh run + new hash.

Standing rule inherited from the exchange: any proposed addition that does not change
a predicted observable is deleted.

Nature decides who pays.
