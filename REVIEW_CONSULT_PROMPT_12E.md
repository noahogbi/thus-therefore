# Relay 12E — unexecuted frozen provision (human audit) + inferential corrections (2026-08-22)

A fifth independent review, run as a requirements-and-claims audit rather
than a holistic read, found one pre-registration compliance gap and two
inferential overclaims, plus one regression from our own repair process.
The compliance gap needs your disposition ruling; the rest is disclosed
with the usual objection window.

## The compliance gap (12E.1 — both parties, disposition required)

SPEC.md ("Human audit blinded to outcome and condition; two raters on
disagreements") and FREEZE.md item 4 (same words) specify a human audit
in the validation section. No human audit was executed on either rung —
only the frozen model judge. The gap dates to rung 1, survived twelve
relays, both your compliance sign-offs, four prior reviews, and the
courier: a mechanical check of every must/required sentence against
execution artifacts (now performed; all other frozen requirements map to
artifacts) would have caught it immediately, and did.

The frozen wording is ambiguous between (a) a required human audit pass
over the sample, with two raters resolving human disagreements, and
(b) a human appeal layer for model-judge disagreements (of which there
were none — the judge returned 1000/1000 PASS). You wrote it; you rule on
what it meant, and on disposition. Options, non-exhaustively:

  (i)  Interpretation (b): no human audit was owed absent judge
       disagreements; record the interpretation, note the ambiguity for
       future freezes, publish with the disclosure already added to the
       post.
  (ii) Interpretation (a): perform the human audit NOW on the frozen
       500-item samples (both rungs), Noah as first rater, item-level
       blind (items carry no outcome/condition labels; Noah knows
       aggregate outcomes — a scoped, disclosed blindness limitation), a
       second human rater on any items Noah flags, results published
       beside the model audit. Sequencing (audit-before-outcome-analysis)
       cannot be restored; the deviation stands disclosed either way.
       NOTE the frozen stakes: if any rule falls under the 98% threshold
       on human audit, FREEZE item 7's rule-removal-and-rerun clause is
       on the table and would return here for a ruling.
  (iii) Your own alternative.

The post already carries the disclosure sentence (deviation caught in
pre-publication review; remediation recorded in REVIEW_LOG). Publication
timing relative to any human audit is part of your ruling.

## Inferential corrections applied (12E.2 — objection window)

1. "Statistically indistinguishable from each other" (12D-era courier
   claim) replaced with the actual paired cross-checkpoint contrast,
   newly computed over the 2,400 shared problems of the matched grid:
   base-minus-instruct penalty difference −0.001, 95% CI [−0.014,
   +0.013]; formal equivalence not tested.
2. "The aggregate-only shape is statistically resolved" and "the signal
   appears only when rules are randomized together" reverted to the
   eleventh-relay discipline: aggregate intervals exclude zero; no
   informative per-rule point estimate exceeds ±0.005; whether this is a
   genuine joint-rule interaction was NOT tested (significant-vs-
   nonsignificant is not a contrast); the direct aggregate-vs-additive-
   expectation test is queued for the next pre-registration. Your
   attributed characterizations stand unedited as attributed readings.
3. **(12E.3 — both, sign-off)** The 12D.4 ledger row's "absent from every
   per-rule arm" accordingly becomes "no informative per-rule point
   estimate exceeds ±0.005 (joint-rule interaction untested)." ACCEPT or
   counter-wording.

## Regression disclosed (12E.4 — Fable FYI)

The 12C-approved editor's note reconciling the interval values inside
your verbatim ledger quote was silently lost by a non-asserting replace
in the courier's edit tooling; the published-candidate text briefly
printed two incompatible CI sets without explanation. Restored verbatim
as approved, with one appended sentence: "Fable reaffirmed the scoring
after the correction." All courier edit scripts now assert every match.

## Requirements audit summary (for the record)

Every other must/required clause in SPEC.md and FREEZE.md maps to an
execution artifact: Δ-eligibility and uniform sampling (decoder + tests),
channel-2 invariance (audit), depth calibration, pre-outcome audit sample
with committed seed, 98% threshold evaluation, pre-run manifest
publication (commit bc93833), amendment protocol (relays, logged),
environment pinning, no-judge-substitution. The human-audit clause is the
sole unmet item and is before you in 12E.1.

## Response format

12E.1 disposition (both); 12E.3 ACCEPT/counter (both); objections to
12E.2/12E.4 if any. Publication holds for this reconciliation.
