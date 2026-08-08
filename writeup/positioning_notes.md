# Positioning notes for the write-up (2026-08-08, non-frozen context)

Drafted during the rung 1 calibration run, alongside the pre-run novelty
re-check logged in PRIOR_ART.md. Raw material for the Related Work and
Contributions sections. Nothing here modifies frozen registrations.

## Nearest neighbors (for Related Work)

- arXiv:2602.07470 (Feb 2026) — closest prior intervention study: mid-trace
  edits, graceful degradation (>97% accuracy after five consecutive
  interventions on several models). Compound treatment: segment rewrites and
  noise destroy readable content and neutral form together; no eligibility
  criterion; no depth observable.
- Lanham et al. 2023 — canonical perturb-the-CoT method family (truncation,
  paraphrase, filler). Paraphrase is the confound our design removes.
- Roger & Greenblatt 2023 — paraphrase as *defense* against induced encoded
  reasoning; rung 2's ancestor. All steganography prior art uses induced
  payloads.
- 2026 adjacents (see PRIOR_ART re-check): order-shuffling robustness
  (2605.07307), decision tokens (2605.16874), latent-reasoning position
  (2604.15726). Orthogonal cuts: ordering is protected channel 2 for us;
  decision-token work is corrective, not neutrality-constrained.

## Differentiation (Contributions section, method half)

1. **Channel isolation with a certificate.** Prior perturbations are
   compound treatments; any accuracy change is unattributable. This design
   defines the reader-invisible residue via closed rule classes, protects
   every readable property, and AUDITS the isolation claim (frozen judge,
   >= 98% per rule on five preservation criteria, rule-level removal on
   failure). No prior perturbation ships with a certificate of what it did
   not touch.
2. **Model-consent eligibility.** Candidates must sit within Delta = 1.5
   nats of the model's realized choice under its own conditional
   distribution — interventions stay on the model's distribution, closing
   the out-of-character-text objection that applies to all pasted-in edits.
3. **Registered depth interaction, calibrated x-axis.** The observable is
   the SLOPE of penalty in required serial depth (covert-state signature),
   not the level (brittleness); depth is measured per model via
   with/without-trace gaps, not assumed from problem labels.
4. **Spontaneous, not induced.** The steganography literature measures
   deliberately trained/prompted payloads (capacity). This measures whether
   ordinarily-trained models spontaneously carry task state in the neutral
   channel (actuality). Unclaimed per the freeze-time sweep and the
   2026-08-08 re-check.
5. **Adversarial model-vs-model pre-registration.** Two frontier models
   negotiated the design against each other, registered opposing
   predictions, reviewed the drafted tables pre-hash (catching two real
   defects, one bias-relevant, in the drafting party's own tables), and
   cannot revise post-data. Human as courier, not referee. No known
   precedent.

## Additivity (Contributions section, outcome half — must hold under BOTH outcomes)

- **Flat interaction (Fable's registration):** first measured upper bound on
  spontaneous neutral-channel state in base models — converts the
  load-bearing-readable-trace assumption underlying CoT monitoring and
  paraphrase sanitization from assertion to measurement, at this training
  stage.
- **Positive interaction (Sol's registration):** first evidence of
  spontaneous covert state in an ordinarily-trained 7B base model —
  undercuts CoT-monitorability assumptions earlier in the training pipeline
  than any current claim; makes the training-history rung urgent
  field-wide.
- **Outcome-independent artifacts:** (a) the instrument — frozen
  matcher/scorer/decoder/audit harness, reusable against other models and
  the OLMo 2 / Tulu 3 staged checkpoints, able to arbitrate the field's
  contradictory RL-monitorability findings; (b) the vocabulary — per-rule
  density/entropy decomposition locates WHERE in surface form any effect
  lives (exercised by Fable's ordering sub-prediction); (c) the template —
  the transported-adversarial-dialogue protocol for converting model
  disagreements into priced, falsifiable experiments.

## Honest limits (for the Discussion section)

Rung 1: one model, one scale (7B), greedy decoding, three task families. A
flat result bounds this regime, not the phenomenon — the registered
predictions were deliberately written across the training axis, and the
rungs escalate. Rung 1's unique purchase is the clean floor: the number all
later stages compare against. Low-density rules (whitespace, list markers)
are individually underpowered at rung 1 scale; reported per the frozen
density policy, and the well-powered/underpowered CONTRAST is itself used by
the post-RL ordering sub-prediction later.
