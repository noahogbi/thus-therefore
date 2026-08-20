# IDEAS_FOR_NEXT_PREREGISTRATION.md

Per CLAUDE.md rule 3: improvements and extensions noticed during frozen work
are logged here, not acted on. Two sections: supplementary proposals that can
run under the CURRENT framework (with party blessing, after registered
results are delivered), and experiments that require a NEW pre-registration.

## Supplementary proposals for the tenth relay (current data / new arms,
## never pooled with registered observables)

Proposed 2026-08-20, before the O1/O2 analysis ran; to be put to both
parties in the tenth relay. Run only if blessed, only after the frozen
analysis is delivered, always labeled exploratory/descriptive.

1. **Watermark-capacity report (free, descriptive).** From the native
   exposure pass: eligible sites per trace, nats within Delta = 1.5 at each,
   totals by rule and cell — a measured upper bound on sampling-watermark
   capacity in the reader-neutral channel of instruct CoT. Extends S1.
   Relevance: watermarking deployments (writeup/watermarking_context.md);
   the 2.45% density result suggests the number is small, which is itself
   the finding.
2. **Trace-position decomposition (free, descriptive).** Distribution of
   intervened-site positions within traces, especially distance from
   termination. Connects rule-05's answer-region mechanism to the
   answer-only-watermarking caveat quantitatively.
3. **Real-watermark bridge arm (~$25-40, new generation).** Same 8-cell
   grid, native vs. published watermark schemes at standard strength
   (Kirchenbauer green-list delta~2; keyed near-tie re-settling a la
   SynthID/Anthropic) applied to the full stream. Bridges the dose
   asymmetry: frozen-harness penalty vs. real-watermark penalty on
   identical problems. New script, new run directories, frozen artifacts
   untouched. First direct watermark-on-CoT cost measurement under a
   neutrality-audited baseline.

## Requires a new pre-registration (do NOT bolt on)

- **Multi-turn self-consumption probe (deployment regime 3).** Watermarked
  or neutrally-perturbed output re-entering context as reasoning input for
  a follow-up task; penalty as a function of consumed-trace depth. Models
  the agentic loop where "downstream of CoT" dissolves. Needs its own
  calibration, observables, and registered predictions.
- **Cross-model transport.** The rung 1 / follow-on grids on a second model
  family (e.g. Llama, OLMo staged checkpoints per original rung 4 axis).
- **Extended document-state equivalence audit** (RESULTS.md discussion
  item): reader-side audit extended to whether a substitution changes any
  downstream-parseable document state, not just reader-recovered content.
- **Watermark-strength dose-response.** If the bridge arm (above) is
  interesting, a proper dose axis (delta sweep) with registered functional
  form belongs in the next prereg.
