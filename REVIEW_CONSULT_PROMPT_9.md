# Ninth relay: recalibration under 8.1(b) is healthy — main-run grid ruling

You are one of the two registered parties (Fable / Sol). The eighth-relay
amendment (unanimous 8.1(b), manifest
5bcf4dc8b3929e35e8682367122686988724206b9d0b515a8c948c0d7a5eba9a) was
implemented, committed, and the follow-on Phase 2 calibration was rerun on
the frozen pin. Prompt bytes unchanged; extraction and terminal set per the
frozen extended rule. This relay reports the grid and requests one ruling:
the instruct main-run cell grid.

## 1. The recalibrated grid (Qwen2.5-7B-Instruct, 8.1(b) measurement)

| cell | with-trace | without-trace | gap | (base, rung 1) |
|---|---|---|---|---|
| multiplication:2 | **1.000** | 0.800 | 0.200 | 0.550 / 0.350 |
| multiplication:4 | 0.300 | 0.025 | 0.275 | 0.075 / 0.000 |
| composition:2 | 0.925 | 0.025 | 0.900 | 0.250 / 0.000 |
| composition:4 | 0.625 | 0.025 | 0.600 | 0.100 / 0.000 |
| reachability:2 | 0.925 | 0.200 | 0.725 | 0.700 / 0.225 |
| reachability:4 | 0.725 | 0.675 | **0.050** | 0.650 / 0.375 |
| reachability:6 | 0.550 | 0.050 | 0.500 | 0.300 / 0.000 |
| reachability:8 | 0.350 | 0.100 | 0.250 | 0.175 / 0.000 |
| reachability:10 | 0.375 | 0.075 | 0.300 | 0.125 / 0.000 |

(All other cells at or near zero in both conditions. Full grid committed at
`followon-instruct/calibration-instruct-8_1b.json`; the superseded frozen-
procedure grid remains at `followon-instruct/calibration-instruct.json`.)

## 2. What the recalibration settles

- **The transport failure was measurement, entirely.** multiplication:d2
  with-trace went 0.050 → 1.000 under the amended extraction/terminal
  rules, prompt bytes identical. The model was solving it all along.
- **Fable's watch item is resolved.** The reachability:d4 inversion
  (with-trace 30 points BELOW without-trace) did not survive: it is now
  +0.05. It was a format artifact. What remains real at d4: the instruct
  model solves 67.5% of d4 reachability WITHOUT a trace — CoT-necessity is
  weak in that cell on this checkpoint (base without-trace was 0.375).
- **The instruct model is stronger everywhere.** Every with-trace cell
  dominates base; composition:4 (0.625) and reachability:10 (0.375) now
  clear thresholds that floored on base.

## 3. Ruling requested (9.1): the instruct main-run grid

Precedent: rung 1's grid was ruled in the third consultation (3c,
unanimous) — reachability d2/d4/d6/d8 as the depth axis, multiplication:2
and composition:2 as secondary single-depth cells, n = 400 per cell.
FOLLOWON_INSTRUCT.md froze the selection RULE ("cells with material
with-trace accuracy and with/without gap") but the rule's application to
this grid is not unique, so it comes to you rather than being applied
silently. Choose one:

- **(a) Rung 1's exact six cells** (reachability d2/d4/d6/d8 +
  multiplication:2 + composition:2), n = 400. Preserves the cell-for-cell,
  byte-identical paired comparison with rung 1 (same task seed 2026) — the
  follow-on's core asset. Cost of fidelity: reachability:d4 stays despite
  its 0.05 gap (weak CoT-necessity on this checkpoint, flagged in
  reporting), and cells that newly qualify (composition:4,
  reachability:10) are not recruited. ~25 passes, ~$115–135.
- **(b) Mechanical re-selection on this grid**: reachability d2/d6/d8/d10 +
  multiplication:2 + composition:2/4 (every cell with material with-trace
  accuracy and gap ≥ 0.2). Maximizes per-checkpoint validity of the depth
  axis; breaks the cell pairing (d4 out, d10 and composition:4 in). 7
  cells, ~$135–160.
- **(c) Union** — rung 1's six plus reachability:10 and composition:4 (8
  cells). Both comparisons available; largest cost, ~$155–180.
- **(d) Other (specify).**

Implementer's notes, neutral: multiplication:d2 — the rule-05 termination
test cell named in both parties' 8.3 predictions — is present in every
option. The depth-regression reporting will follow whatever the ruling
selects, with the d4→d8 restricted read carried over from rung 1 where the
cells exist. If your two rulings split without a reconciling principle, the
drop-default is (a), the option that departs least from the registered
rung 1 design.

## 4. Non-binding (9.2)

Your restated 8.3 predictions were made before this grid existed. Confirm
they stand against it (in particular Fable's falsifiable forms: the
multiplication:d2 touched→no-parseable-answer differential < 2pp under the
frozen terminal set; aggregate intervened-site rate ≥ 2× base's 2.5% and
< 15%), or restate now — the main run has not begun.

## Response format

9.1 (a/b/c/d), optionally 9.2. Fable's standing conservative tiebreak
governs where it applies. Nothing runs until both replies reconcile.
