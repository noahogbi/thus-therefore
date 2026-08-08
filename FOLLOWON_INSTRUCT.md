# Pre-registered follow-on: light-instruct variation (execution gated on rung 1 base run)

Registered 2026-08-08 per the third-consultation reconciliation (REVIEW_LOG),
BEFORE any intervention data exists — Fable's tightening, adopted under the
standing conservative tiebreak, executing Sol's follow-on proposal with the
design-after-data door closed. This document is the follow-on's design
commitment; its own freeze manifest is generated at its execution time and
must be consistent with this file.

## Specification

- **Model pin:** Qwen/Qwen2.5-7B-Instruct, revision
  a09a35458c702b33eeacc393d103063234e8bc28 (identified and logged
  2026-08-08, before the rung 1 base main run began).
- **Procedure: identical to rung 1 end-to-end.** Same frozen SPEC, rule
  tables (as amended pre-freeze), judge pin and audit protocol, Delta = 1.5,
  arm plan (native + Tier A aggregate + seven per-rule arms), intervention
  seeds [271828, 161803, 141421], audit seed 314159, and n = 400 per cell.
- **Calibration rerun:** the depth grid is NOT inherited from the base run.
  The instruct model gets its own Phase 2 calibration (same protocol, same
  no-trace suffix, generation seed from the frozen list), and its grid is
  selected by the same rule (cells with material with-trace accuracy and
  with/without gap).
- **Manifest:** a new FREEZE_MANIFEST is generated for the follow-on (new
  environment.json pin), published before its first generation run.
- **Execution gate:** nothing in this follow-on runs until the rung 1 base
  main run, audit, and analysis are complete. Only the EXECUTION waits; the
  design is fixed by this document, blind to the base run's outcomes.

## Registration coverage

SPEC section 6's registrations name "base and light-instruct checkpoints"
for the zero-interaction prediction; both parties' second- and third-round
rulings treat the instruct run as a covered follow-on experiment, not a
repair to rung 1. If the two runs disagree, the disagreement is data.
