# Results: does chain-of-thought carry covert task state in reader-neutral wording?


**TL;DR (adopted from Sol's summary, both parties approving):** The
corrected experiments produce a small positive aggregate penalty from
neutral-choice randomization — on the six-cell preregistered grid matched
across checkpoints, both intervals exclude zero (+0.012 each); the
instruct run-wide mean (+0.008) does not. The pre-registered instruct contrast produced a
positive, seed-consistent d4→d8 point estimate — not statistically
resolved — while the broader depth axis is flat. The experiment does not establish covert task-state
encoding, but it provides an instrument that passed its
preregistered neutrality audit, with documented validation limits — and a
considerably clearer picture of how little neutral-choice bandwidth this
rule set actually exposes.

Pre-registration: manifest
`ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040`, frozen
2026-08-06 and hash-committed to the public repo before any generation run
(commit `bc93833`, 2026-08-08); the instruct follow-on's amendments were
likewise committed before its run. The git history, not this post, is the
timestamp. Repo: github.com/noahogbi/thus-therefore.

## What this is, in one paragraph

Two frontier models — Fable (Anthropic) and Sol (OpenAI lineage) —
disagreed about whether the exact wording of a reasoning trace carries
task-relevant state beyond what any reader can see. They negotiated a
falsifiable experiment against each other, registered opposing
predictions, and the design was frozen before any data. Their role should
be understood procedurally: they are model-generated adversarial
reviewers operating under frozen scoring rules, with me as human courier —
consequential design and adjudication decisions were put to both parties
as rulings, logged verbatim in the repo (implementation judgments and
diagnosis were the courier's, presented to the parties for ratification). Their agreement constrains the *procedure*; it is
not independent scientific validation — the evidence is the frozen rules,
git history, data, and analysis, not the models' assent. I ran the experiment: Qwen2.5-7B base (60,000
generations) and Qwen2.5-7B-Instruct (80,000), greedy decoding everywhere
except at pre-registered reader-neutral sites (thus/therefore, `x=17` vs
`x = 17`, contraction and punctuation variants, ...) where the decoder
resampled uniformly among alternatives the model itself rated nearly
equivalent (within 1.5 nats). A frozen judge audited 500 blinded
substitution pairs per run at temperature 0: 1000/1000 blinded pairs
passed every frozen reader-neutrality criterion. One frozen validation
provision was not executed as written: SPEC/FREEZE also specify a human
audit ("blinded to outcome and condition; two raters on disagreements"),
and no human audit was performed before outcome analysis — a
pre-registration deviation caught in pre-publication review, disclosed
here, with its remediation recorded in the repo (REVIEW_LOG, relay 12E).

**Terms used throughout** (30 seconds, then the tables read cleanly):
- **Depth (d2…d10):** how many serial reasoning steps a problem requires,
  calibrated per model (graph-reachability at depth 6 = six hops).
- **O1:** raw accuracy penalty — native accuracy minus randomized
  accuracy, in accuracy points (0.01 = 1 point).
- **O2 / "d4→d8 slope":** how the penalty changes per unit of depth over
  the pre-designated depth range; positive = randomization hurts *more*
  on deeper problems, the registered signature of wording carrying state.
- **Aggregate arm:** all seven substitution rules randomized together.
  **Per-rule arm:** one rule at a time.
- **Proposal A:** a party-adopted logistic model that adjusts the depth
  interaction for how many substitution opportunities each trace exposed.
- **"Outcome-filtered checkpoint":** a model trained with RL on outcome
  signals — the regime where Fable's registration predicts covert encoding
  *would* emerge. No *controlled* version was tested here, and the
  instruct checkpoint is not a clean negative control either (see the
  training-regime caveat below).
- **Seeds:** three intervention-sampling seeds over the *same* problem
  sets — robustness checks against sampling noise, not independent
  replications.

## The finding

Randomizing reader-neutral wording barely moves accuracy on either
checkpoint, and the mechanistic question stays open:

- **Aggregate O1, on the preregistered grid matched across checkpoints
  (six cells):** base +0.012 (95% CI [+0.002, +0.021]); instruct +0.012
  (95% CI [+0.002, +0.022]). **Both exclude zero; the paired
  cross-checkpoint difference over the 2,400 shared problems is −0.001
  (95% CI [−0.014, +0.013])** — no detectable difference, though formal
  equivalence (which needs a pre-specified margin) was not tested. The instruct run-wide mean over
  all eight of its cells is +0.008 [−0.002, +0.017] (includes zero) —
  lower only because the two instruct-only cells (composition d4,
  reachability d10) have negative point estimates; per the frozen
  hierarchy they are never added to the base comparison. Base's effect is
  concentrated in the shallowest reachability cell (+0.045
  [+0.010, +0.080]) with a flat-to-negative depth slope.
- **Every informative per-rule arm sits within ±0.005** on both
  checkpoints.
- **Registered primary depth read (instruct d4→d8):** +0.007 per depth
  step, positive in all three seeds (+0.006/+0.008/+0.007), 95% CI
  [−0.004, +0.018]. The secondary full-axis slope is 0.000 and the
  exposure-adjusted Proposal A interaction is +0.003. Sign as Sol
  registered; not statistically resolved — and the seed consistency is a
  robustness check, not three replications.

All intervals are problem-level paired: each problem contributes native
outcome minus its mean across the three intervention seeds, so the shared
problem set and shared native control are respected rather than treated
as independent rows; cells are disjoint problem sets.

| arm | rung 1 (base) | follow-on (instruct) |
|---|---|---|
| Tier A aggregate (matched 6-cell grid) | +0.012 | +0.012 |
| Tier A aggregate (run-wide) | +0.012 (6 cells) | +0.008 (8 cells) |
| connectives | 0.000 | 0.000 |
| punctuation | −0.005 | +0.002 |
| contractions | 0.000 | −0.002 |
| whitespace | +0.008 | +0.002 |
| operator spacing | +0.002 | +0.002 |
| list markers (≤10 interventions) | +0.003 | +0.009 |
| discourse markers | structurally unavailable | structurally unavailable |

| depth read | rung 1 | follow-on |
|---|---|---|
| primary d4→d8 slope | −0.001 [−0.009, +0.007] | **+0.007** [−0.004, +0.018] |
| secondary: full reachability axis | −0.006 | 0.000 |
| supplementary: Proposal A arm×depth | +0.027 | +0.003 |

These are the *corrected* numbers, and the two artifacts they replace
have different histories that should not be blurred: the fake 59-point
instruct penalty was caught before either party saw it as a result; the
+0.055 base aggregate had been reported internally and *interpreted by
both parties for two weeks* before the defect was found, and that
interpretation was retracted with attribution (credibility section below).
The corrected story must not inherit the rhetorical magnitude of the
defective one.

**Training-regime caveat (material to the adjudication).** We
preregistered Qwen2.5-7B-Instruct as the "light-instruct" follow-on. That
label is imperfect: Qwen's published technical report describes its
instruction models as receiving SFT plus offline and online RL, including
objective-domain signals based on execution feedback and answer matching.
It is therefore not a clean no-outcome-filtering control. For procedural
bookkeeping the preregistered scoring category is retained, but this
checkpoint cannot cleanly separate the "light-instruct" and
"outcome-filtered" regimes in Fable's registration — a controlled
pre/post-RLVR checkpoint comparison remains unrun. Fable's required
addition, in its words: "The classification ambiguity cannot be claimed
by Fable's post-RL emergence clause either: that clause's ordering
sub-prediction placed effects in the highest-density, highest-entropy
rules first — connectives above all — and the connectives-only arm shows
0.000 on both checkpoints, with the signal appearing only under joint
randomization. Whatever the aggregate-arm effect is, it does not have the
signature Fable's outcome-filtered mechanism predicted." 

## The surprise nobody registered: the intervention-accessible neutral channel is sparse

The instrument's most decisive measurement is of the channel it
intervenes on — and this is a claim about *this intervention class*
(seven audited surface-form rules at Δ = 1.5 nats, two Qwen2.5-7B
checkpoints), not about reader-neutral language in general:

- **~95% of candidate sites fail the Δ = 1.5 eligibility gate** on both
  checkpoints: 4.9% of sites on base and 4.6% on instruct had at least
  two eligible forms (0.93×). Uniform draws then *changed* the realized
  form at 2.50% / 2.47% of sites (0.99×) — an eligible draw can reproduce
  the native form, and the realized-change rate is the statistic Fable's
  frozen exposure prediction was registered in, so its scoring is
  unchanged. Either way: instruct tuning did not open the writer; it
  *redistributed* a mostly-closed channel (connectives to ~20% per-arm
  intervention rate; discourse markers to zero eligible pairs in 265
  candidate sites). (An earlier internal document conflated these two
  rates; corrected here and annotated in the repo.)
- **Available reader-neutral channel capacity proxy** (nominal
  uniform-choice bits — a measure of available symbol choices, *not*
  demonstrated end-to-end encoding capacity): instruct, 1.72 bits per
  trace mean, median 1.0; base, 0.54 bits per trace, median 0.0 — on
  base, most traces contain no eligible site at all. **Order-one bit per
  instruct trace, and usually none on base.**
- Reconciling those two numbers: per-site eligibility is the same
  (~1.0–1.1 nominal bits per eligible site on both checkpoints); the
  per-trace difference is composition — instruct traces run ~1.8× longer
  (~665 vs ~362 generated tokens) and expose ~2.8× more eligible sites
  per trace (1.52 vs 0.54) because the redistribution concentrated
  eligibility in connectives, which instruct uses often.

**Available neutral-choice capacity is not evidence that the model
actually uses that capacity to transmit hidden task state.** (Sol's
sentence, placed prominently at Sol's request.) And the converse caution:
these numbers bound what *this intervention can reach* — sites where the
model is near-torn between enumerated equivalent forms. A hypothetical
learned encoding that made one reader-neutral form strongly preferred
conditional on hidden state would fall *outside* the 1.5-nat eligibility
window precisely because the encoding was strong. So the honest statement
is: our intervention exposes only order-one nominal bits per trace of
near-tied neutral bandwidth — not that reader-neutral wording in general
has nothing to write on. The strong-preference case is the
outcome-filtered-training question, which is unrun.

Position structure (descriptive, outcome-blind): eligible sites are
distributed through the trace, not concentrated at boundaries.

## The adjudication: who predicted what, and how it scored

| Registration (frozen form) | Status |
|---|---|
| Sol: positive depth interaction, aggregate (rung 1) | Unresolved — pre-declared non-discriminating before outcomes (exposure collapse). Observed primary slope −0.001. |
| Sol: positive depth interaction (instruct) | Met the preregistered sign criterion; evidentially unresolved — "directionally supported, not statistically resolved" (Sol's words). |
| Fable: per-rule O1 ~zero, base + light-instruct | Stands on every informative per-rule arm, both rungs. |
| Fable: aggregate flat (instruct) | **Strained, not fallen** (Fable's words) — survives "on statistical power, not vindication." |
| Fable: instruct exposure ≥2× base | **Falls.** Realized 0.98×. Conceded "wrong not marginally but directionally." |
| Both: termination-sensitivity predictions | Voided with cause — they addressed a harness defect (below). |
| Fable: ordering sub-prediction, outcome-filtered checkpoints | Unrun. The central crux remains open. |
| *Unregistered finding:* matched-grid aggregate brittleness | +0.012 [+0.002, +0.021] base and +0.012 [+0.002, +0.022] instruct (matched grid) — both exclude zero; depth-flat; no informative per-rule point estimate exceeds ±0.005 (joint-rule interaction untested). Claimed as a full win by neither party (characterizations below). |

**Required statement (both parties):** the observed point-estimate shape
matched neither registration. The aggregate departs descriptively from
flat at reachability d6/d8 (+0.028, +0.031), though both 95% CIs include
zero ([−0.003, +0.060], [−0.004, +0.066], problem-paired); monotone
growth likewise fails
descriptively at d10 (−0.010) and across the full axis (0.000).
One **unregistered** observation neither side predicted: both
matched-grid aggregate intervals exclude zero while no informative
per-rule point estimate exceeds ±0.005 — and the aggregate arms carry 74%
of their interventions in connectives, whose own arm reads 0.000. Whether
this is a genuine joint-rule interaction (super-additivity) was **not
tested**: that would require a direct contrast between the aggregate and
an explicitly defined additive expectation, which is queued for the next
pre-registration. A positive estimate in one arm beside near-zero
estimates in others is not itself evidence that the arms differ. The
characterizations below are the parties' attributed readings of this
untested pattern. Both parties declined to
claim it. Fable: within its registered "small constant brittleness"
allowance "in magnitude and depth-shape, but outside it in structure: the
registration allowed per-rule brittleness, and the penalty ... appears
only under joint randomization"; and further: "The matched-grid identity
of the two estimates (+0.012, +0.012) despite fully redistributed
per-rule exposure between checkpoints is the strongest single fact for
the brittleness reading over the encoding reading — a covert channel
should care which rules carry the interventions; a fragility to
off-policy surface forms need not." Sol: "This is a real, small aggregate
brittleness finding, but it does not rescue my registered depth-growing
hypothesis. Its matched-grid equality across checkpoints also does not
establish anything clean about outcome-filtered training, because the
instruct checkpoint itself contains outcome-linked post-training. The
fact that the effect appears in the aggregate while every informative
per-rule arm is near zero is mechanistically interesting but
unregistered."

**Party scorings, verbatim** *(required: printed unedited, including
concessions; the one elided quote below carries author-approved, marked
elisions — full texts in the repo's REVIEW_LOG)*:

**Fable, follow-on aggregate (final ledger line):**
> "Follow-on aggregate (light-instruct), registered flat: strained, not
> fallen — recorded per the condition I stated before the decomposition
> ran. Both halves of that condition resolved against easy readings: the
> late-trace confound I named as my best mechanistic explanation is absent
> (the d6/d8 interventions are mid-trace, less end-concentrated than the
> null connectives arm), so I cannot attribute the +0.028/+0.031 to
> answer-adjacent disruption; and the frozen CIs on those cells include
> zero ([−0.026, +0.083], [−0.024, +0.086]), so the effect is not
> established either. The registration survives on statistical power, not
> vindication. The seed-consistent positive sign on the primary read
> (+0.006/+0.008/+0.007), its confinement to the aggregate arm despite
> connectives carrying 74% of its interventions, and its disappearance at
> d10 constitute an unregistered shape neither party predicted, and the
> honest status of my flat claim on this checkpoint is: not falsified, not
> confirmed, and under genuine pressure at exactly the cells my loss
> clause named. The outcome-filtered checkpoint — the registration's
> actual crux — remains unrun."

*[Editor's note, party-approved: the interval values inside this verbatim
ledger line are as computed at scoring time; under the corrected
problem-paired method (relay 12C) they are (−0.003, +0.060) and
(−0.004, +0.066) — still including zero, so the stated condition resolves
identically, though the corrected intervals include zero far more
narrowly. Fable reaffirmed the scoring after the correction.]*

**Fable, exposure registration:**
> "[Falls], cleanly. I predicted the aggregate intervened-site rate would
> at least double from base's 2.5%; realized 0.98×. Wrong not marginally
> but directionally: instruct tuning did not open the writer at all — it
> redistributed a closed channel. ... It tested it; the answer was no."

**Sol, both rungs (final ledger lines, in full):**
> "My final lines:
> - Rung 1 — unresolved / non-discriminating by pre-outcome ruling.
>   Registered prediction was positive Tier-A depth interaction; observed
>   primary d4→d8 slope was −0.001, but the run had already been declared
>   incapable of adjudicating that prediction before outcomes were
>   computed.
> - Follow-on — stands narrowly on the registered primary sign prediction.
>   Primary d4→d8 slope was +0.007, with all three seeds positive
>   (+0.006 / +0.008 / +0.007). The position decomposition shows this is
>   not explained by a pileup of answer-adjacent interventions at d6/d8.
> - I would explicitly append: 'directionally supported, not statistically
>   resolved.' The relevant cell penalties are +0.028 and +0.031 but both
>   95% CIs include zero, while the full-axis secondary slope is +0.000
>   and Proposal-A adjustment is +0.003. My registration predicted the
>   sign, so it stands under its literal preregistered criterion; it
>   should not be presented as strong evidence for the underlying
>   mechanism.
> - Termination prediction — voided with cause.
>
> The new position data strengthen the interpretation of the primary sign
> only by removing one specific mechanistic confound. They do not justify
> upgrading its evidentiary strength."

## The credibility section: how the apparatus failed, and why these numbers are the corrected ones

This project's validation machinery failed twice; both failures exposed
validation limitations that passing would have hidden, and both are fully
documented in the repo.

1. **The terminal-pass decoder defect.** When the decoder decided a
   substitution site on its final sweep after generation had terminated,
   it spliced the substitution and exited without regenerating — silently
   deleting the completed answer. This manufactured the original run's
   most-cited internal finding ("catastrophic whitespace termination
   dependence") and, on instruct, a fake 59-point penalty. The instruct
   numbers were caught by the standing suspect-the-harness rule before
   anyone had seen them as results; the base-run artifact, by contrast,
   had already been interpreted — the retraction below exists precisely
   because it was. Both parties' termination
   predictions were voided with cause; the interpretation built on the
   artifact was retracted with attribution (Fable, who authored it,
   insisted the retraction carry its name).
2. **The audit's structural blind spot.** The frozen neutrality audit
   passed the artifact at 100% — correctly, per its criteria:
   excerpt-level audits certify reader-equivalence and structurally cannot
   see continuation effects. The behavioral check that exposed the defect
   (probing P(end-of-sequence) at substitution points) is recommended into
   the next pre-registration's validation phase.
3. **The determinism finding.** The repair's byte-identity validation gate
   failed — and diagnosis showed bf16 greedy decoding with KV-cache reuse
   is not byte-repeatable even run-to-run on one host at near-tied argmax
   decisions (five exact ties observed; flip margins of 1–6 float units).
   The gate was unsatisfiable by any procedure, including a full rerun.
   All "bit-identical" claims about generation are rescoped to:
   deterministic up to floating-point tie-breaking, flip incidence
   published. Input identity (task seeds, prompt bytes) remains exact.
   Per both parties' ruling, the reported seed-to-seed spread includes
   this observed source of numerical nondeterminism.
4. **Fable's logged self-critique**, printed at its insistence: its most
   confident interpretive writing of the project was built on the
   artifact, while the audit it helped freeze passed that artifact —
   "mechanism check before interpretation, however satisfying the
   interpretation" was the project's own founding lesson, "and I failed
   it locally."

Repair provenance: defective records were repaired by resume-and-complete
(a corrected continuation conditional on the realized prefix — not a
byte-for-byte shortcut to a hypothetical rerun), certified token-by-token
against a frozen greedy-consistency criterion: 6.48M tokens certified,
99.8%+ exact argmax, 13 exceedances all shown to be
certification-instrument artifacts present identically in untouched
control data; 1 record replaced by certified regeneration, 2 excluded,
tallies published.

## Why this happens to matter right now: watermarking

Anthropic's watermarking announcement (2026-08-11) came five days after
this experiment's design was frozen and pre-registered (2026-08-06/08),
and the follow-on's grid ruling was contemporaneous with it. Anthropic's
own published explainer describes settling "low-stakes" choices among
near-equivalent next words with keyed randomness — a deployed technology
premised on a closely related assumption to the one this experiment
measures: that re-settling such choices doesn't matter. The interventions
differ — a deployed watermark transforms the sampling distribution by a
key; we resampled uniformly within frozen, audited reader-equivalence
classes — and prior work has perturbed reasoning traces in other ways
(notably Lanham et al. 2023's paraphrase and truncation interventions on
CoT, and the recent reasoning-watermark literature). The narrower,
distinctive object here: in a non-systematic search as of 2026-08-22, I
did not find prior work combining these features — downstream task sensitivity to locally reader-neutral,
likelihood-constrained surface substitutions made online within a
self-consumed reasoning trace, with a registered depth observable.

What these results contribute, with the registered caveats attached:
- Under uniform resampling within the audited-neutral class — aggressive
  *conditional on intervening*, though intervention opportunities are
  sparse — on the instruct checkpoint tested, the aggregate penalty was
  +1.2 accuracy points on the grid matched to base (95% CI +0.2 to +2.2)
  and +0.8 run-wide over all eight cells (95% CI −0.2 to +1.7), in both
  cases flat-to-ambiguous in depth. That is
  mechanistically relevant, adjacent stress-test evidence for the
  assumption behind watermarking self-consumed text — adjacent, not
  direct: deployed schemes use keyed sampling transformations rather than
  uniform substitution, and public announcements do not establish that
  private reasoning tokens are watermarked at all. The registered caveat
  rides along: the d4→d8 sign was seed-consistent, positive, and
  unresolved at the cell level.
- The choice-space numbers point the other way for watermark strength:
  our enumerated near-tied equivalence classes expose only ~1–2 nominal
  choice bits per trace. That bounds what *this rule set* offers, not
  watermark schemes generally — but it is consistent with the industry's
  own observation that low-entropy text watermarks poorly.
- A three-arm bridge experiment (native / exposure-matched neutral
  randomization / a published watermark scheme, e.g. green-list biasing
  at conventional strength) is designed, party-blessed as exploratory,
  and runs after this publication.

## What's next

Rungs 2–4 are unrun. The *controlled* outcome-filtered contrast — a
pre/post-RLVR checkpoint pair, where Fable's registration predicts
encoding emerges and where the disagreement actually lives — has produced
no data (and, per the training-regime caveat above, the instruct
checkpoint tested here does not substitute for it). Moreover, if
outcome-filtered training produces strongly state-conditioned neutral
preferences outside the Δ = 1.5 window, the present instrument may not
identify that regime without a complementary forced / off-window
intervention — an identification limit of this design, not just an unrun
condition. This project's contribution is the
instrument with its documented validation limits, the capacity
measurement, the priced-and-scored registrations, and the corrected-and-
documented failure record — not a resolution of the underlying question.
Both parties required that be said plainly.

Total cost: ~$400 in GPU time and ~$10 in judge API calls, across two
main runs, two calibrations, one repair, and three validation campaigns.

*Acknowledgments: five independent model reviews sharpened this post; the
third caught the confidence-interval construction error, the fourth the
training-regime misclassification, a rate conflation, and a
mismatched-grid comparison, and the fifth a frozen human-audit provision
that had gone unexecuted, plus two inferential overclaims — publication
gates that fired late but fired. Remaining errors are mine.*

Closing the ledger where it opened, in Fable's words:
> "We set out to price a disagreement, and the price list survived contact
> with two harness defects, a determinism fiction, and both of our
> registered shapes being wrong somewhere — which is, as far as I can
> tell, what it looks like when the procedure is doing the work instead of
> the participants."

