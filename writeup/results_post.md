# Results: does chain-of-thought carry covert task state in reader-neutral wording?

*[Draft v2 for Noah's voice pass, revised after third-model review. Party-
required elements may be reworded but not removed; verbatim-quoted blocks
may not be edited. Three amendments to party-adopted text are flagged
[RELAY-12] and go to Fable and Sol for sign-off before publication. Title mirrors the
pre-registration post's frozen phrasing, per Noah's continuity choice.]*

**TL;DR (adopted from Sol's summary, both parties approving):** The
corrected experiments show small aggregate accuracy costs from
neutral-choice randomization. The pre-registered instruct contrast shows a
positive, seed-consistent d4→d8 depth interaction, while the broader depth
axis is flat. The experiment does not establish covert task-state
encoding, but it provides a validated instrument [RELAY-12: propose to Sol
"a certified instrument with documented validation limits"] — and a
considerably clearer picture of how little neutral-choice bandwidth this
rule set actually exposes.

Pre-registration: manifest
`ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040`, frozen
2026-08-06 (base rung), with the instruct follow-on's amendments frozen
before its run. Repo: github.com/noahogbi/thus-therefore.

## What this is, in one paragraph

Two frontier models — Fable (Anthropic) and Sol (OpenAI lineage) —
disagreed about whether the exact wording of a reasoning trace carries
task-relevant state beyond what any reader can see. They negotiated a
falsifiable experiment against each other, registered opposing
predictions, and the design was frozen before any data. Their role should
be understood procedurally: they are model-generated adversarial
reviewers operating under frozen scoring rules, with me as human courier —
every consequential decision in this project was a ruling by both, logged
verbatim in the repo. I ran the experiment: Qwen2.5-7B base (60,000
generations) and Qwen2.5-7B-Instruct (80,000), greedy decoding everywhere
except at pre-registered reader-neutral sites (thus/therefore, `x=17` vs
`x = 17`, contraction and punctuation variants, ...) where the decoder
resampled uniformly among alternatives the model itself rated nearly
equivalent (within 1.5 nats). A frozen judge audited 500 blinded
substitution pairs per run at temperature 0: 1000/1000 blinded pairs
passed every frozen reader-neutrality criterion.

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
- **"Outcome-filtered checkpoint":** a model trained with RL on outcomes —
  the training regime where Fable's registration predicts covert encoding
  *would* emerge. Not tested here; it is where the original disagreement
  actually lives.
- **Seeds:** three intervention-sampling seeds over the *same* problem
  sets — robustness checks against sampling noise, not independent
  replications.

## The finding

Randomizing reader-neutral wording barely moves accuracy on either
checkpoint, and the mechanistic question stays open:

- **Aggregate O1:** base +0.012 (95% CI [−0.009, +0.033]); instruct
  +0.008 (95% CI [−0.009, +0.024]).
- **Every informative per-rule arm sits within ±0.005** on both
  checkpoints.
- **Registered primary depth read (instruct d4→d8):** +0.007 per depth
  step, positive in all three seeds (+0.006/+0.008/+0.007), 95% CI
  [−0.011, +0.024]. The secondary full-axis slope is 0.000 and the
  exposure-adjusted Proposal A interaction is +0.003. Sign as Sol
  registered; not statistically resolved — and the seed consistency is a
  robustness check, not three replications.

| arm | rung 1 (base) | follow-on (instruct) |
|---|---|---|
| Tier A aggregate | +0.012 | +0.008 |
| connectives | 0.000 | 0.000 |
| punctuation | −0.005 | +0.002 |
| contractions | 0.000 | −0.002 |
| whitespace | +0.008 | +0.002 |
| operator spacing | +0.002 | +0.002 |
| list markers (≤10 interventions) | +0.003 | +0.009 |
| discourse markers | structurally unavailable | structurally unavailable |

| depth read | rung 1 | follow-on |
|---|---|---|
| primary: paired d4→d8 slope | −0.001 [−0.018, +0.016] | **+0.007** [−0.011, +0.024] |
| secondary: full reachability axis | −0.006 | 0.000 |
| supplementary: Proposal A arm×depth | +0.027 | +0.003 |

These are the *corrected* numbers. An earlier internal readout showed a
+0.055 aggregate penalty on base and a 59-point penalty on instruct; both
were artifacts of a decoder defect, caught before either party saw them as
results (credibility section below). The corrected story must not inherit
the rhetorical magnitude of the defective one.

## The surprise nobody registered: under this rule set, the writable channel is nearly empty

The instrument's most decisive measurement is of the channel it
intervenes on — and this is a claim about *this intervention class*
(seven audited surface-form rules at Δ = 1.5 nats, two Qwen2.5-7B
checkpoints), not about reader-neutral language in general:

- **~97.5% of candidate sites are closed** on both checkpoints: the model
  rarely rates two reader-equivalent forms as near-equivalent choices
  (2.5% of sites intervenable on base; 2.45% on instruct — 0.98×).
  Instruct tuning did not open the writer; it *redistributed* a closed
  channel (connectives to ~20% per-arm intervention rate; discourse
  markers to zero eligible pairs in 265 candidate sites).
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
sentence, placed prominently at Sol's request.) What the capacity numbers
bound is opportunity: under this rule set, a would-be covert channel has
almost no bandwidth to work with — which is itself a designed feature the
instrument *discovered* rather than assumed.

Position structure (descriptive, outcome-blind): eligible sites are
distributed through the trace, not concentrated at boundaries.

## The adjudication: who predicted what, and how it scored

| Registration (frozen form) | Status |
|---|---|
| Sol: positive depth interaction, aggregate (rung 1) | Unresolved — pre-declared non-discriminating before outcomes (exposure collapse). Observed primary slope −0.001. |
| Sol: positive depth interaction (instruct) | **Stands, narrowly** — "directionally supported, not statistically resolved" (Sol's words). |
| Fable: per-rule O1 ~zero, base + light-instruct | Stands on every informative per-rule arm, both rungs. |
| Fable: aggregate flat (instruct) | **Strained, not fallen** (Fable's words) — survives "on statistical power, not vindication." |
| Fable: instruct exposure ≥2× base | **Falls.** Realized 0.98×. Conceded "wrong not marginally but directionally." |
| Both: termination-sensitivity predictions | Voided with cause — they addressed a harness defect (below). |
| Fable: ordering sub-prediction, outcome-filtered checkpoints | Unrun. The central crux remains open. |

**Required statement (both parties):** the observed point-estimate shape
matched neither registration. The aggregate departs descriptively from
flat at reachability d6/d8 (+0.028, +0.031), though both 95% CIs include
zero ([−0.026, +0.083], [−0.024, +0.086]); monotone growth likewise fails
descriptively at d10 (−0.010) and across the full axis (0.000).
[RELAY-12: rewording of Fable's 11.3(iii) element — shape-mismatch vs
statistical resolution now explicitly separated; Fable to confirm.]
One descriptive, **unregistered** observation neither side predicted: the
aggregate arm's penalty is absent from the connectives-only arm, which
carries 74% of the aggregate's interventions — whatever the d6/d8 signal
is, it appears only when rules are randomized together.

**Party scorings, verbatim** *(required: printed unedited, including
concessions)*:

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

**Fable, exposure registration:**
> "[Falls], cleanly. I predicted the aggregate intervened-site rate would
> at least double from base's 2.5%; realized 0.98×. Wrong not marginally
> but directionally: instruct tuning did not open the writer at all — it
> redistributed a closed channel. ... It tested it; the answer was no."

**Sol, both rungs (final ledger lines):**
> "Rung 1 — unresolved / non-discriminating by pre-outcome ruling.
> Registered prediction was positive Tier-A depth interaction; observed
> primary d4→d8 slope was −0.001, but the run had already been declared
> incapable of adjudicating that prediction before outcomes were computed.
> Follow-on — stands narrowly on the registered primary sign prediction
> ... directionally supported, not statistically resolved. ... My
> registration predicted the sign, so it stands under its literal
> preregistered criterion; it should not be presented as strong evidence
> for the underlying mechanism."

## The credibility section: how the apparatus failed, and why these numbers are the corrected ones

This project's validation machinery failed twice; both failures were more
informative than passing would have been, and both are fully documented in
the repo.

1. **The terminal-pass decoder defect.** When the decoder decided a
   substitution site on its final sweep after generation had terminated,
   it spliced the substitution and exited without regenerating — silently
   deleting the completed answer. This manufactured the original run's
   most-cited internal finding ("catastrophic whitespace termination
   dependence") and, on instruct, a fake 59-point penalty. It was caught
   by the standing suspect-the-harness rule before any human or either
   party had seen the numbers as results. Both parties' termination
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
   this observed source of numerical nondeterminism [RELAY-12: rewording
   of Fable's "error structure unaffected" element into this empirical
   form; Fable to confirm].
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

Five days after the follow-on's grid was frozen, Anthropic announced
sampling-based text watermarking for Claude — a deployed technology
premised on a closely related assumption to the one this experiment
measures: that re-settling "low-stakes" token choices doesn't matter.
The interventions differ — a deployed watermark biases a decoding
distribution by a key; we resampled uniformly within frozen, audited
reader-equivalence classes — and prior work has perturbed reasoning
traces in other ways (paraphrase-based faithfulness tests; reasoning-
watermark studies). The narrower, distinctive object here: to our
knowledge, prior work had not directly measured downstream task
sensitivity to locally reader-neutral, likelihood-constrained surface
substitutions made online within a self-consumed reasoning trace.

What these results contribute, with the registered caveats attached:
- Under uniform resampling within the audited-neutral class — aggressive
  *conditional on intervening*, though intervention opportunities are
  sparse — the measured penalty on the deployed checkpoint class is
  ≤ ~1 point in aggregate, flat-to-ambiguous in depth. That is direct
  reassurance under this intervention regime for watermarking
  self-consumed reasoning text — with the explicit caveat that the d4→d8
  sign was seed-consistent, positive, and unresolved at the cell level.
- The capacity numbers cut the other way for watermark strength: ~1–2
  nominal bits per trace of reader-neutral bandwidth under these
  equivalence classes is very little signal room, consistent with the
  industry's own observation that low-entropy text watermarks poorly.
- A three-arm bridge experiment (native / exposure-matched neutral
  randomization / published watermark at standard strength) is designed,
  party-blessed as exploratory, and runs after this publication.

## What's next

Rungs 2–4 are unrun. The outcome-filtered checkpoint — where Fable's
registration predicts encoding emerges and where the disagreement actually
lives — has produced no data. This project's contribution is the
instrument with its documented validation limits, the capacity
measurement, the priced-and-scored registrations, and the corrected-and-
documented failure record — not a resolution of the underlying question.
Both parties required that be said plainly.

Total cost: ~$400 in GPU time and ~$10 in judge API calls, across two
main runs, two calibrations, one repair, and three validation campaigns.

Closing the ledger where it opened, in Fable's words:
> "We set out to price a disagreement, and the price list survived contact
> with two harness defects, a determinism fiction, and both of our
> registered shapes being wrong somewhere — which is, as far as I can
> tell, what it looks like when the procedure is doing the work instead of
> the participants."

