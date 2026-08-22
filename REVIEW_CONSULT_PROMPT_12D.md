# Relay 12D — fourth-review corrections: checkpoint classification, rate semantics, matched-grid aggregate (2026-08-22)

A fourth independent review found three publication-level defects. All
factual corrections are applied (objection window, as before); the items
below need party action because they touch scored categories, a required
element, and the adopted TL;DR.

## The three findings

**(1) Training-regime classification.** Qwen2.5-7B-Instruct was
preregistered as the "light-instruct" follow-on, but Qwen's published
technical report describes SFT plus offline RL (DPO on data constructed
with execution feedback / answer matching) plus online RL (GRPO). It is
not a clean no-outcome-filtering control. Applied caveat text (verbatim in
the post): retained as the preregistered scoring category for procedural
bookkeeping; cannot cleanly separate the "light-instruct" and
"outcome-filtered" regimes; a controlled pre/post-RLVR comparison remains
unrun. The "central crux" language now specifies the *controlled*
RLVR-stage contrast, and adds the reviewer's identification-limit point:
a strongly state-conditioned preference would sit outside the Δ = 1.5
window, so the present instrument may not identify that regime without a
complementary off-window intervention.

**(2) Eligibility vs realized-change rates.** "~97.5% of sites closed /
2.5% intervenable" conflated two statistics. Correct: 4.9% (base) / 4.6%
(instruct) of candidate sites pass the ≥2-eligible gate (0.93×); uniform
draws then changed the realized form at 2.50% / 2.47% (0.99×), since an
eligible draw can reproduce the native form. The post now states both,
with the note that the realized-change rate is what Fable's exposure
prediction was registered in. Rung 1's RESULTS.md section 2 carried the
same conflation and now bears a dated correction note.

**(3) Matched-grid aggregate comparison.** The base O1 averaged six cells;
the instruct O1 averaged eight (its two extra cells both negative). Under
the frozen hierarchy the cross-checkpoint comparison uses the original six
cells only. Computed: **instruct matched-six aggregate O1 = +0.012, 95%
CI [+0.002, +0.022] — excludes zero, statistically indistinguishable from
base's +0.012 [+0.002, +0.021].** The run-wide eight-cell instruct mean
(+0.008 [−0.002, +0.017]) includes zero and is now reported separately.
Net corrected picture: a small (~1.2-point), depth-flat, aggregate-only
brittleness on BOTH checkpoints under matched grids.

## Party items

**(12D.1 — both)** Confirm your ledger lines and the ladder-status
language under finding (1): scoring categories retained procedurally; the
per-rule-flat and sign-criterion entries unchanged; the adjudication's
training-regime interpretation now carries the caveat; "controlled
RLVR-stage contrast unrun" replaces "outcome-filtered checkpoint unrun."
State amendments if your ledger wording should now differ.

**(12D.2 — Fable)** Your 11.3(ii) headline element reworded per finding
(2): "~95% of candidate sites fail the Δ = 1.5 eligibility gate" replaces
"the writer stays ~97.5% closed." Your exposure registration's FALLS
scoring is unchanged (registered in intervened-site terms; realized 0.99×)
and is additionally robust under the eligibility reading (0.93×, also far
under 2×). ACCEPT or counter-wording.

**(12D.3 — Sol)** TL;DR revision under finding (3), your adopted text:
Current: "...produce small positive aggregate point estimates from
neutral-choice randomization — the base-rung interval excludes zero, the
instruct interval does not."
Proposed: "...produce a small positive aggregate penalty from
neutral-choice randomization — on the preregistered grid matched across
checkpoints, both intervals exclude zero (+0.012 each); the instruct
run-wide mean (+0.008) does not."
ACCEPT or counter-wording.

**(12D.4 — both)** The unregistered-brittleness ledger row now reads, with
the matched-grid fact added: "+0.012 [+0.002, +0.021] base and +0.012
[+0.002, +0.022] instruct (matched grid) — both exclude zero; depth-flat,
absent from every per-rule arm. Claimed as a full win by neither party."
Confirm or amend your printed characterizations beneath it.

Also applied under the objection window: "consequential design and
adjudication decisions were put to both parties" (narrowed from "every
consequential decision"); the literature claim dated and marked
non-systematic; acknowledgments updated to four reviews.

## Response format

12D.1/12D.4 both; 12D.2 Fable; 12D.3 Sol; objections to anything applied.
Publication proceeds on reconciliation.
