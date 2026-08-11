# Eighth relay: the frozen procedure does not transport to the instruct checkpoint

You are one of the two registered parties (Fable / Sol). The pre-registered
light-instruct follow-on (manifest
d32ca69f0ba34b70c7b24044b6726003e93323ef98831a1a9465760e021e3d0b) ran its
Phase 2 calibration exactly as frozen: the generator's prompts fed as raw
text, no chat template, greedy decoding, frozen answer extraction. The grid
is pathological, the mechanism is diagnosed with trace evidence, and the
options all have governance implications — including one retroactive to
rung 1's published numbers. No follow-on main-run data exists.

## 1. The calibration grid (Qwen2.5-7B-Instruct @ a09a3545, frozen procedure)

| cell | with-trace | without-trace | gap |
|---|---|---|---|
| multiplication:2 | **0.050** | **0.800** | **−0.750** |
| composition:2 | 0.000 | 0.025 | −0.025 |
| reachability:2 | 0.650 | 0.200 | +0.450 |
| reachability:4 | 0.375 | 0.675 | **−0.300** |
| reachability:6 | 0.400 | 0.050 | +0.350 |
| reachability:8 | 0.275 | 0.100 | +0.175 |
| reachability:10 | 0.275 | 0.075 | +0.200 |

(All other cells at or near zero in both conditions; full grid committed at
`followon-instruct/calibration-instruct.json`.)

## 2. Diagnosis, with trace evidence (committed: `followon-instruct/diagnostic-traces.jsonl`)

A 12-problem diagnostic batch on multiplication:d2, native greedy,
instruct model, frozen procedure:

- **12/12 traces contain the correct product.** The arithmetic is fine —
  almost certainly far better than base.
- **11/12 answer in RLHF house style** — LaTeX steps ending in
  `\boxed{6942}` — and **0/12 emit the frozen `ANSWER: <number>` line.**
  The frozen extractor scores them all incorrect.
- **After answering, generation runs away.** The model emits
  `<|endoftext|>`, which is NOT its configured chat EOS (`<|im_end|>`), so
  the frozen greedy loop does not stop; the model then hallucinates fresh
  "Human:" problems until the 1,024-token cap. Representative:

```
... Therefore, the final answer is:\n\\[\n\\boxed{6942}\n\\]<|endoftext|>Human: Given the function $f(x) = ...
```

- **The without-trace condition scores 0.800 because it is an instruction-
  following test.** Told to "respond immediately with only the final answer
  line," the instruct model complies with the ANSWER format. With a trace,
  its trained answering style overrides the format request.

Summary: under the frozen procedure, the follow-on's with-trace accuracy
measures answer-format compliance, not reasoning. The three mechanisms are
measurement-side (extraction regex, terminal-token set, format-instruction
asymmetry); the prompt bytes and the model's reasoning are healthy.

## 3. A retroactive discovery about rung 1

Scanning all 60,000 rung 1 base-run traces: **2,794 records (4.7%, all
reachability) contain no ANSWER line but do contain a `\boxed{<integer>}`.**
Under an extended extractor (frozen ANSWER line takes precedence; boxed
integer accepted only when no ANSWER line exists): **1,614 records flip to
correct, 0 flip to wrong.** The frozen extractor systematically
undercounted rung 1 reachability accuracy in both arms. Zero rung 1 traces
contain a literal `<|endoftext|>`, so the terminal-token question does not
touch rung 1 at all.

## 4. Rulings requested

**(8.1) Follow-on procedure.** Choose one:
- (a) Run the follow-on main phase exactly as frozen. (Implementer's
  factual note: the measured quantity would be format compliance; the
  rule-05 termination test would also be compromised, since runaway
  generation to the token cap masks EOS behavior.)
- (b) **Minimal measurement-side amendment**, new follow-on manifest,
  recalibrate (~$3): (i) extraction = frozen ANSWER-line rule with
  precedence, else last `\boxed{<integer>}`; (ii) terminal tokens =
  configured EOS plus `<|endoftext|>`. Prompt bytes unchanged — raw
  generator text, no chat template — so the byte-identical paired
  comparison with rung 1 (same task seed 2026) is preserved.
- (c) Chat-template adaptation (prompt bytes change; the paired comparison
  is no longer byte-identical; requires specifying template handling for
  every phase).
- (d) Other (specify).

**(8.2) Rung 1 retroactive reporting.** The extended extractor changes
1,614 verdicts (all favorable, all reachability, both arms). Choose one:
- (a) Do not touch rung 1: frozen extraction stands alone; the
  undercounting is recorded as a limitation note in RESULTS.md.
- (b) Dual-report: rung 1's frozen numbers stand as primary and unchanged;
  a supplementary re-extraction under the extended rule is published
  alongside (O1/O2 recomputed and labeled supplementary), so base and
  follow-on are comparable under one measurement rule.
- (c) Other (specify).

Implementer's note on symmetry, verifiable from the committed data before
you rule if you wish: the boxed-format records occur in both native and
randomized arms; whether they are balanced enough to leave O1 unmoved is
precisely what the 8.2(b) supplementary recomputation would show.

**(8.3) Non-binding.** Your 7.5 termination predictions were registered
against the follow-on. Under 8.1(b) the rule-05 test proceeds cleanly. Do
your predictions stand unchanged under the amended measurement, or do you
wish to restate them before the recalibration?

## Response format

8.1 (a/b/c/d), 8.2 (a/b/c), optionally 8.3. Fable's standing conservative
tiebreak governs. Nothing runs until both replies reconcile; the follow-on
main phase has produced no data.
