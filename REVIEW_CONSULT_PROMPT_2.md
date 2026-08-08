# Second consultation: one implementation note and the arm plan (final pre-hash items)

You are being consulted as one of the two registered parties (Fable / Sol) to
the frozen "Neutral-Choice Randomization Experiment (Rung 1)". Your earlier
dispositions (F1–F5) were reconciled and applied as logged in REVIEW_LOG.md;
status since then: the full harness is implemented and tested (matcher,
eligibility scorer with the F5 two-region semantics, intervention decoder,
depth calibrator, blinded audit sampler, O1/O2 analysis — 114 tests), the
judge smoke test PASSED (claude-opus-4-5-20251101 served the exact
audit-shaped request at temperature 0, thinking off, well-formed verdict),
and Noah has signed off on the post-amendment site review. Two items remain
before hashing. Fable's standing tiebreak (adopt the more conservative
option where rulings differ) will again govern reconciliation.

## Item 1 — IN-1: the initiation set is undecidable mid-generation (confirm or amend)

Building the decoder surfaced a temporal-knowledge gap of the same species
as F1. Rule 03's initiation set ("First," / "To start," / "To begin,")
carries this frozen exclusion:

> "conservative: exclude 'First,' set entirely whenever the trace contains
> explicit ordinal enumeration (First/Second/Third)"

"Whenever the trace contains" is TRACE-GLOBAL. But interventions happen
during generation: at the moment a "First," site is decided, text produced
LATER could still introduce "Second, ..." and retroactively flip the
exclusion — after a randomized "First," -> "To start," had already broken
enumeration parallelism (channel 2; this is the review hunt list's own
example). The decoder therefore NEVER randomizes the initiation set during
generation, logging such sites with skip_reason
"global_exclusion_undecidable_mid_generation" and reporting the set as
structurally unavailable during generation (mirroring the F1 treatment of
the sequencing set). The table is untouched.

**Ruling requested — choose one:**
- (IN-1a) Confirm the conservative skip. The initiation set's generation-
  time density is a structural zero (reported as such, never as an observed
  zero penalty). No table change.
- (IN-1b) Amend to a decidable-at-decision-time rule (e.g. "exclude when
  the trace SO FAR contains ordinal enumeration") — specify exact wording,
  and note this accepts the residual leak the hunt list warned about.
- (IN-1c) Something else (specify).

## Item 2 — Arm plan and seed count for the main run

The harness supports per-rule arms: a run may randomize all Tier A rules
together, or any single rule in isolation (overlap resolution always runs
over all rules first, so a rule's site inventory is identical across arms).
This matters because SPEC section 2 registers O1/O2 "separately per rule",
which is only cleanly measurable when one rule is randomized alone, while
the section 6 aggregate predictions reference the Tier A aggregate.

GPU cost is small at every option (rented RTX 4090; roughly $5–$45 across
the plans below), so treat this as a scientific-completeness question, with
one caveat: low-density rules (whitespace, list markers) will be
individually underpowered at rung-1 scale no matter the arm plan — their
per-rule density and power are reported per the frozen policy either way.

**Ruling requested — choose one arm plan and a seed count:**
- (2a) Aggregate arm only: native + all-rules-randomized.
- (2b) Aggregate + all seven per-rule arms (native + 8 randomized arms).
- (2c) Aggregate + a named subset of per-rule arms (e.g. the high-density
  rules: connectives, operator spacing, contractions) — specify which.
- Seeds: how many intervention seeds per randomized arm (1–3)? More seeds
  tighten the estimate of the randomization distribution at linear cost.

Also for the record, the proposed committed seeds are nothing-up-my-sleeve
constants: intervention_sampling_seed = 271828, audit_sample_seed = 314159.
Object now or they freeze.

## Response format

Reply with numbered dispositions for Item 1 (IN-1a/b/c) and Item 2 (arm
plan letter + seed count + seed-constant objection if any). Anything not
ruled on remains as described. After both parties' replies are reconciled,
seeds and environment are finalized, the manifest is hashed, the repo goes
public, and the pre-registration post is published with the hash — then the
GPU run begins.
