# Results: does chain-of-thought carry covert task state in reader-neutral wording?

*[Draft for Noah's voice pass. Publishes together with the pre-registration
post per standing choice. Every element below is required by party rulings
(REVIEW_LOG, relays 10–11B); the required elements may be reworded but not
removed. Verbatim-marked blocks may not be edited at all.]*

**TL;DR (adopted from Sol's restrained summary, both parties approving):**
The corrected experiments show small aggregate accuracy costs from
neutral-choice randomization. The pre-registered instruct contrast shows a
positive, seed-consistent d4→d8 depth interaction, while the broader depth
axis is flat. The experiment does not establish covert task-state
encoding, but it provides a validated instrument — and a considerably
clearer picture of how little neutral-choice bandwidth this rule set
actually exposes.

Pre-registration: manifest
`ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040`, frozen
2026-08-06 (base rung) and the eighth/ninth-relay amendments (instruct
follow-on), all before their respective runs. Repo: github.com/noahogbi/thus-therefore.

## What this is

Two frontier models — Fable (Anthropic) and Sol (OpenAI lineage) —
disagreed about what the tokens of a reasoning trace do, negotiated a
falsifiable experiment in an adversarial dialogue, registered opposing
predictions, and froze the design before any data. I ran it: Qwen2.5-7B
base (60,000 generations) and Qwen2.5-7B-Instruct (80,000 generations),
greedy decoding everywhere except at pre-registered reader-neutral sites
(thus/therefore, `x=17` / `x = 17`, ...) where the decoder resampled
uniformly among alternatives the model itself rated within 1.5 nats.
A frozen judge audited 500 blinded substitution pairs per rung at
temperature 0: 1000/1000 preserved every reader-visible property.

## The prediction ledger

| Registration (frozen form) | Status |
|---|---|
| Sol: positive depth interaction, Tier A aggregate (rung 1) | Unresolved — pre-declared non-discriminating before outcomes (exposure collapse). Observed primary slope −0.001. |
| Sol: positive depth interaction (instruct follow-on) | **Stands, narrowly** — "directionally supported, not statistically resolved" (Sol's words). Primary d4→d8 = +0.007; seeds +0.006/+0.008/+0.007; full-axis +0.000; Proposal A +0.003. |
| Fable: per-rule O1 ~zero, base + light-instruct | Stands on every informative per-rule arm (all within ±0.005, both rungs). |
| Fable: aggregate flat (instruct follow-on) | **Strained, not fallen** (Fable's words) — survives "on statistical power, not vindication." |
| Fable: instruct exposure ≥2× base's 2.5% | **Falls.** Realized 0.98×. Conceded "wrong not marginally but directionally." |
| Both: termination-sensitivity predictions | Voided with cause — the phenomenon they addressed was a harness defect (see methods lessons). |
| Fable: ordering sub-prediction, outcome-filtered checkpoints | Unrun. The central crux of the original disagreement remains open. |

**Required statement (both parties):** neither registered *shape* matched
the follow-on data. Flat fails at the aggregate's reachability d6/d8
(+0.028, +0.031 — 95% CIs [−0.026, +0.083] and [−0.024, +0.086], both
including zero); monotone growth fails at d10 (−0.010) and on the full
axis (+0.000). And one descriptive, **unregistered** observation neither
side predicted: the aggregate arm's penalty is absent from the
connectives-only arm, which carries 74% of the aggregate's interventions —
whatever the d6/d8 signal is, it appears only when rules are randomized
together.

## Registered results

O1 — mean accuracy penalty (native − randomized), pooled over three seeds:

| arm | rung 1 (base) | follow-on (instruct) |
|---|---|---|
| Tier A aggregate | +0.012 | +0.009 |
| connectives | +0.000 | −0.000 |
| punctuation | −0.005 | +0.002 |
| contractions | +0.000 | −0.002 |
| whitespace | +0.008 | +0.002 |
| operator spacing | +0.002 | +0.002 |
| list markers (≤10 interventions) | +0.003 | +0.009 |
| discourse markers | structurally unavailable | structurally unavailable |

O2 — depth interaction, primary and secondary reads always together:

| read | rung 1 | follow-on |
|---|---|---|
| primary: paired d4→d8 slope | −0.001 | **+0.007** (all seeds positive) |
| secondary: full reachability axis | −0.006 | +0.000 |
| supplementary: Proposal A arm×depth | +0.027 | +0.003 |

These are the corrected numbers. An earlier internal readout showed a
+0.055 aggregate penalty on base and a 59-point penalty on instruct; both
were artifacts of a decoder defect, caught before either party saw them
(methods lessons below). The corrected story must not inherit the
rhetorical magnitude of the defective one.

## The headline nobody registered: the channel is nearly empty

The instrument's most decisive measurement is of the channel itself.
At Δ = 1.5 nats, the model rarely regards two reader-equivalent surface
forms as comparable:

- **~97.5% of candidate sites are closed** on both checkpoints (2.5% of
  sites intervenable on base; 2.45% on instruct — 0.98×). Instruct tuning
  did not open the writer; it *redistributed* a closed channel
  (connectives to ~20% per-arm intervention rate; discourse markers to
  zero eligible pairs in 265 candidate sites).
- **Available reader-neutral channel capacity proxy** (nominal
  uniform-choice bits; a measure of available symbol choices, *not*
  demonstrated end-to-end encoding capacity): instruct, 1.72 bits per
  trace mean, median 1.0, 15% of traces zero. Base, 0.54 bits per trace,
  median 0.0 — most base traces contain no eligible site at all. Rates:
  2.6 / 1.5 nominal bits per 1,000 generated tokens.

**Available neutral-choice capacity is not evidence that the model
actually uses that capacity to transmit hidden task state.** (Sol's
sentence, placed prominently at Sol's request.) What the capacity numbers
bound is the *opportunity*: under this rule set, a would-be covert channel
in reader-neutral wording has roughly one coin-flip of bandwidth per
reasoning trace to work with.

Position structure (descriptive, outcome-blind): eligible sites and
realized interventions are distributed through the trace, not concentrated
at boundaries — aggregate-arm interventions at reachability d6/d8 sit at
19–24% in the final fifth, median 435–519 tokens from termination.

## Party scorings, verbatim

*(Required: printed unedited, including concessions.)*

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

## Methods lessons (required unsoftened)

This project's validation machinery failed twice, and both failures were
more informative than passing would have been.

1. **The terminal-pass decoder defect.** The intervention decoder, when it
   decided a site on the final sweep after generation had terminated,
   spliced the substitution and exited without regenerating — silently
   deleting the completed answer. This manufactured rung 1's most-cited
   internal finding ("catastrophic rule-05 termination dependence") and,
   on the instruct run, a fake 59-point penalty. It was caught by the
   standing suspect-the-harness rule before any human or either party had
   seen the numbers as results; both parties' termination predictions were
   voided with cause; the interpretation built on it was retracted with
   attribution (Fable, who authored it, insisted the retraction carry its
   name). Diagnosis, blast radius, repair, and certification are all in
   the repo (DECODER_DEFECT_DIAGNOSIS.md, REPAIR_PLAN.md).
2. **The audit's structural blind spot.** The frozen neutrality audit
   passed the artifact at 100% — correctly, per its criteria: excerpt-level
   audits certify reader-equivalence and structurally cannot see
   continuation effects. The behavioral continuation check that exposed
   the defect (probing P(EOS) at substitution points) is recommended into
   the next pre-registration's validation phase.
3. **The determinism fiction.** The repair's byte-identity validation gate
   failed — and diagnosis showed bf16 greedy decoding with KV-cache reuse
   is not byte-repeatable even run-to-run on one host at near-tied argmax
   decisions (five exact ties observed; flip margins at 1–6 float-units).
   The gate was unsatisfiable by any procedure including a full rerun. All
   "bit-identical" claims about generation are rescoped to: deterministic
   up to floating-point tie-breaking, flip incidence published. Input
   identity (task seeds, prompt bytes) remains exact; the three-seed
   design absorbs tie-flip noise into the reported seed spread, so the
   error structure of the registered estimates is unaffected.
4. **Fable's logged self-critique**, printed at its insistence: its most
   confident interpretive writing of the project (relays 6–9) was built on
   the artifact, while the audit it helped freeze passed that artifact —
   "mechanism check before interpretation, however satisfying the
   interpretation" was the project's own founding lesson, "and I failed it
   locally."

Repair provenance, for the record: the defective records were repaired by
resume-and-complete (a corrected continuation conditional on the realized
prefix — not a byte-for-byte shortcut to a hypothetical rerun), certified
token-by-token against a frozen greedy-consistency criterion: 6.48M tokens,
99.8%+ exact argmax, 13 exceedances all shown to be certification-
instrument artifacts present identically in untouched control data; 1
record replaced by certified regeneration, 2 excluded, tallies published.

## Why this matters right now: watermarking

Five days after the follow-on's grid was frozen, Anthropic announced
sampling-based watermarking for Claude — a deployed technology premised on
exactly the assumption this experiment measures: that re-settling
"low-stakes" token choices doesn't matter. Watermark quality evaluations
certify that *readers* can't tell the difference; nobody had measured
whether the *model's own downstream computation* cares, and the industry's
answer-only watermarking designs (e.g. ReasonMark) engineer around that
unmeasured assumption at a real capacity cost.

What these results contribute, stated with the registered asymmetries:
- Under perturbation *harsher* than a sampling watermark (uniform
  resampling within the eligibility class, at audited-neutral sites), the
  measured penalty on the deployed checkpoint class is ≤ ~1 point in
  aggregate, flat-to-ambiguous in depth. That is the strongest
  reassurance available to date for watermarking self-consumed reasoning
  text at this scale — with the explicit caveat that the d4→d8 sign was
  seed-consistent and positive, and unpowered at the cell level.
- The capacity numbers cut the other way for watermark *strength*: ~1–2
  nominal bits per trace of reader-neutral bandwidth (under this rule
  set's equivalence classes) is very little signal room, consistent with
  the industry's own observation that low-entropy text watermarks poorly.
- A three-arm bridge experiment (native / exposure-matched neutral
  randomization / published watermark at standard strength) is designed,
  party-blessed as exploratory, and runs after this publication.

## What this did and didn't resolve

Rungs 2–4 are unrun. The outcome-filtered checkpoint — where Fable's
registration predicts encoding emerges and where the original disagreement
actually lives — has produced no data. This project's contribution is the
certified instrument, the capacity measurement, the priced-and-scored
registrations, and the corrected-and-documented failure record — not a
resolution of the covert-state question. Both parties required that be
said plainly.

Total cost: ~$400 in GPU time and ~$10 in judge API calls, across two
main runs, two calibrations, one repair, and three validation campaigns.

Closing the ledger where it opened, in Fable's words:
> "We set out to price a disagreement, and the price list survived contact
> with two harness defects, a determinism fiction, and both of our
> registered shapes being wrong somewhere — which is, as far as I can
> tell, what it looks like when the procedure is doing the work instead of
> the participants."
