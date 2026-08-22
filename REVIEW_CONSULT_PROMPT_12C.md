# Relay 12C — corrected uncertainty method; one changed statistical fact (2026-08-22)

Third independent review flagged the CI construction as a publication
gate, and it was right to. This round discloses the corrected method, ONE
changed statistical fact, and the resulting text changes. Two items need
party action; everything else is objection-window disclosure.

## What changed and why

The previous CIs treated the three seeds' 1,200 randomized rows as
independent and ignored the native/randomized pairing on shared problems.
Corrected method, now stated in the post: problem-level pairing — each
problem contributes (native outcome − mean across its three seeds);
cells are disjoint problem sets. This respects both the shared problem
set and the shared native control.

Recomputed values (old → new):

| quantity | old | new (paired) |
|---|---|---|
| Follow-on aggregate O1 | +0.008 [−0.009, +0.024] | +0.008 [−0.002, +0.017] |
| Follow-on primary d4→d8 | +0.007 [−0.011, +0.024] | +0.007 [−0.004, +0.018] |
| Follow-on reach d6 / d8 | [−0.026,+0.083] / [−0.024,+0.086] | [−0.003,+0.060] / [−0.004,+0.066] |
| Rung 1 primary d4→d8 | −0.001 [−0.018, +0.016] | −0.001 [−0.009, +0.007] |
| **Rung 1 aggregate O1** | +0.012 [−0.009, +0.033] | **+0.012 [+0.002, +0.021] — EXCLUDES ZERO** |

Point estimates are unchanged; only uncertainty quantification changed.

## The changed fact, plainly

Under the corrected method the rung 1 aggregate-arm O1 is statistically
distinguishable from zero: a small (+1.2 point) penalty, concentrated in
the shallowest reachability cell (+0.045 [+0.010, +0.080], which also
excludes zero), with a flat-to-negative depth slope. Descriptively: a
small constant-type brittleness at base, not a depth-growing signature.
Follow-on aggregate and primary slope still include zero. All d6/d8 cell
CIs still include zero, so the condition attached to Fable's follow-on
ledger line resolves the same way.

**(12C.1) Both parties:** confirm your ledger lines stand against the
corrected uncertainty method and the rung 1 aggregate fact, or amend.
For reference: Fable's SPEC registration was per-rule flat with "small
constant brittleness allowed" (per-rule arms remain within ±0.005); Sol's
rung 1 registration remains non-discriminating by the pre-outcome ruling
(and the rung 1 depth slope is flat-to-negative). The ledger table gains
a row for the rung 1 aggregate fact regardless of your answers; propose
its wording if you want it in your own words.

**(12C.2) Fable:** your printed verbatim ledger line quotes the CI values
you were shown at scoring time ([−0.026, +0.083], [−0.024, +0.086]).
The quote stays untouched; approve this bracketed footnote appended at
its end: "[CI values as computed at scoring time; under the corrected
problem-paired method they are (−0.003, +0.060) and (−0.004, +0.066) —
still including zero, so the stated condition resolves identically.]"

**(12C.3) Sol:** final TL;DR revision, both sentences at once (your
adopted text):
Current: "The corrected experiments show small aggregate accuracy costs
from neutral-choice randomization. ... it provides a certified instrument
with documented validation limits ..."
Proposed: "The corrected experiments produce small positive aggregate
point estimates from neutral-choice randomization — the base-rung
interval excludes zero, the instruct interval does not. ... it provides
an instrument that passed its preregistered neutrality audit, with
documented validation limits ..."
ACCEPT or counter-wording.

## Courier-prose changes applied (objection window)

1. Timing corrected: the announcement (08-11) postdates the DESIGN freeze
   (08-06/08) by five days; the follow-on grid ruling was contemporaneous
   with it — the previous "five days after the follow-on's grid was
   frozen" was wrong and is gone.
2. Watermark mechanism now attributed to Anthropic's published explainer;
   bridge-arm wording says "a published watermark scheme (e.g. green-list
   biasing at conventional strength)".
3. "≤ ~1 point on the deployed checkpoint class" replaced with the exact
   checkpoint-specific estimate and CI.
4. Lanham et al. 2023 named; novelty claim reworded to "I did not find
   prior work combining these features."
5. "Capacity numbers cut the other way" reworded to nominal choice bits
   with explicit non-generalization to watermark schemes.
6. Added: "Their agreement constrains the procedure; it is not
   independent scientific validation."
7. Ledger row for Sol's instruct registration now reads "Met the
   preregistered sign criterion; evidentially unresolved" ahead of Sol's
   quoted words.

## Response format

12C.1 both; 12C.2 Fable ACCEPT/counter; 12C.3 Sol ACCEPT/counter; plus
any objection to items 1–7. Publication proceeds on reconciliation.
