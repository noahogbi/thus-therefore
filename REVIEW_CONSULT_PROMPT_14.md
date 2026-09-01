# Fourteenth relay — publication sequencing: as-run results now, six-rule rerun as pre-committed follow-up (2026-09-01)

You are one of the two parties (Fable / Sol) to the frozen neutral-choice
randomization experiment. The thirteenth relay is executed: rule 07 removed
whole, both per-rule arms dropped, new manifests generated and committed
(rung 1 `4a48c9fb7d630dc360380dae224b2adbda2159dc5aa623985bb7aa4ed26fe724`,
follow-on `313ed911db50a4bef7ac4a4c2eb9d17238d8d87bfa7c5ed245e85d25bba7eedb`),
matcher guards R7 absence, RUNBOOK allocates 22 passes/rung.

**This relay does not relitigate the rerun.** Sol's (a) governs via Fable's
pre-committed tiebreak deference; the rerun is ordered and stays ordered.
The question here is publication *sequencing only*.

## The situation

- The rerun is staged but not started: it is gated on a ~$350–400 top-up,
  and its wall-clock cost is multiple days. The first launch attempt
  (2026-08-26, ~$6 balance) spent $0.32 and failed on infrastructure —
  a broken-CUDA community host served four times, then a secure pod never
  exposed SSH. Nothing was generated; nothing was lost.
- The principal can fund the rerun but prefers, if the protocol permits,
  to decouple that spend and delay from publication of the work already
  complete, rather than leave publication open-endedly coupled to funding.
- The prereg post and results post are TEXT FINAL per relays 12D/12E.
  The 2026-08-27 schedule addendum set a soft publication target of
  mid-to-late September 2026.

## Why sequencing is genuinely open rather than already ruled

Two texts bear on it and they do not say the same thing:

1. **12E:** "PUBLICATION HOLDS until the audit completes and results are
   published beside the model audit." The human audit is now complete
   (rater 1 998/1000; rater 2 blind-concordant 20/20 with 18 embedded
   decoys), and its results would be published beside the model audit in
   any stage-1 text. On its own terms, 12E's condition is satisfied.
2. **FLEET_STATE (implementer-authored summary, 2026-08-26):**
   "Publication held until rerun + audits (model AND human, both raters)
   + analyses + final relay." This is the implementer's conservative
   reading of the thirteenth relay's sequence, not quoted ruling text.
   The thirteenth relay's disposition orders what is rerun and what is
   published *as provenance vs. as the registered result*; it does not in
   terms rule on whether the already-final posts may go up before the
   rerun completes.

If either party regards the sequencing as already ruled by 13, say so and
this relay ends there.

## 14.1 — the question

**(a) Two-stage publication.** Stage 1, now: publish the prereg post
unchanged, and the results post as executed (seven-rule run), with a
party-governed addendum that at minimum:

  i.   reports the rule-07 human-audit failure exactly as the thirteenth
       relay recorded it — 0/2 on rung 1, judge-passed, rater-2
       blind-concordant; Sol's "overturned [the judge] on Rule 07"
       wording; Fable's sample-size clause; the embedded-decoy sentence;
  ii.  states that rule 07 is removed whole per FREEZE item 7 and that
       ALL randomized arms are being rerun on both rungs on the six-rule
       table under the corrected protocol;
  iii. publishes both rerun manifest hashes (above), so stage 2 is
       pre-committed and tamper-evident before any rerun token is
       generated — the follow-up cannot be quietly dropped or reshaped
       without that being visible against this stage-1 text;
  iv.  labels every as-run randomized number as superseded-with-notice
       provenance (the thirteenth relay's own category), never as the
       registered result of the six-rule protocol, and commits to a
       stage-2 follow-up post reporting the six-rule registered analyses
       whatever they show.

Stage 2, after rerun + judge determinism gate + model audits + human
audit per 12E protocol + frozen analyses: a final relay re-affirms the
ledger against the rerun numbers before the follow-up posts.

**(b) Keep the hold.** Publication waits for the rerun, audits, analyses
and final relay, as the implementer's summary states.

**(c) Another disposition you specify.**

## Considerations both ways (implementer's accounting; weigh or discard)

For (a): the prereg post's entire value is frozen-time text and is
rerun-independent. The as-run randomized numbers are already
superseded-with-notice under the thirteenth relay's own publication plan —
stage 1 publishes nothing the ruling did not already order published as
provenance. The registered outcomes were flat on both rungs, which
weakens any selective-timing account of publishing now. The staged
manifests are committed, so the stage-2 commitment is mechanically
checkable. Fable's thirteenth-relay position — excision is structurally
side-effect-free and the rerun's marginal content is the nondeterminism
floor — implies stage-1 numbers are unlikely to be contradicted, though
Fable deferred on the rerun itself and that deference is not reopened.

Against (a): readers of stage 1 anchor on as-run numbers from a run that
included a rule the human audit invalidated, however labeled; a stage-2
divergence, if the nondeterminism floor surprises, reads publicly as a
walk-back; the hold has protocol-weight precisely because it is
inconvenient, and converting it under funding pressure has
protocol-erosion optics — Sol's thirteenth-relay rationale ("we should
take the cost we precommitted ourselves to") extends naturally, though
not necessarily, to taking the *delay* we precommitted ourselves to. If
that extension governs, rule (b).

## 14.2 — if (a): the addendum's authorship

Specify whether the stage-1 addendum (i)–(iv) may be worded by the
implementer subject to the 12D no-edit zones (party-required elements
reworded but not removed; verbatim-quoted scoring blocks and Fable's
closing sentence untouched), or requires party-approved text verbatim
before posting.

## Standing constraints unaffected by this relay

Credential rotation (PUBLISH_CHECKLIST phase 0) gates any publication
under every disposition. Nothing in this prompt edits any frozen
artifact. Prior datasets and results remain preserved and published as
provenance per the thirteenth relay regardless of the ruling here.
