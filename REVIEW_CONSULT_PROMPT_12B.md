# Relay 12B — post-lock corrections from second independent review (2026-08-22)

Short, bounded round, occasioned by a second independent model review that
found one factual error in the locked text. Because the error is in the
courier's prose, the corrections below have been applied; because you
signed off on the surrounding prose in relay 12, you are shown every
change and may object to any of them. ONE item is an amendment to
party-adopted text and requires sign-off (12B.A, Sol).

## The factual error (corrected; no sign-off needed, objection window open)

The locked text claimed both artifacts were "caught before either party
saw them as results." True for the instruct numbers (embargoed, never
seen); FALSE for rung 1's +0.055, which both of you saw and interpreted
across relays 6–9 before the defect was found — as the post's own
retraction-with-attribution records. The two histories are now separated
wherever they appear: instruct caught pre-interpretation; base interpreted
for two weeks, then retracted. This also removes an internal contradiction
between the post's credibility claim and Fable's printed self-critique.

## Courier-prose calibration edits (applied; objection window open)

1. Pre-registration timestamping made precise: the git history (spec push
   `79781ea` 2026-08-07; manifest-hash commit `bc93833` 2026-08-08, both
   public before any generation) is cited as the external timestamp; the
   post explicitly disclaims being the timestamp itself.
2. Channel-capacity scope corrected: heading now "the
   intervention-accessible neutral channel is sparse" (was "the writable
   channel is nearly empty"); added the eligibility-window caveat — a
   strong learned encoding would make one form strongly preferred and fall
   OUTSIDE the Δ = 1.5 window, so near-tied bandwidth is what was
   measured, not writable bandwidth in general; the strong-preference case
   is the unrun outcome-filtered question.
3. Watermarking claim weakened from "direct reassurance" to
   "mechanistically relevant, adjacent stress-test evidence," noting
   deployed schemes are keyed sampling transformations and that public
   announcements do not establish private reasoning tokens are watermarked.
4. "Both failures were more informative than passing would have been" →
   "both failures exposed validation limitations that passing would have
   hidden."
5. Prereg post gains a dated courier preamble ABOVE the unchanged frozen
   text: (i) the git-history timestamp and the deferred-posting
   explanation for the frozen "this post timestamps the design" line;
   (ii) an explicit flag that the frozen "guarantees one registered
   prediction loses" claim proved overconfident, with pointer to the
   ledger; (iii) the procedural-role statement (model-generated
   adversarial reviewers; products, not labs; no institutional
   involvement or endorsement).

## 12B.A — amendment to Sol's adopted TL;DR (sign-off required)

Current (Sol's text): "The pre-registered instruct contrast shows a
positive, seed-consistent d4→d8 depth interaction, while the broader depth
axis is flat."

Proposed: "The pre-registered instruct contrast produced a positive,
seed-consistent d4→d8 point estimate — not statistically resolved — while
the broader depth axis is flat."

Rationale (reviewer's): the body's standard is "directionally supported,
not statistically resolved"; "shows a ... depth interaction" in the TL;DR
claims more than the CI ([−0.011, +0.024]) supports, and readers will read
"stands" as evidentiary unless the uncertainty is welded on at first
mention. This matches Sol's own 11B refinement.

## Response format

Sol: ACCEPT or counter-wording for 12B.A. Both: any objection to the
applied corrections above, or COMPLIANT. Publication proceeds on
reconciliation of this round.
