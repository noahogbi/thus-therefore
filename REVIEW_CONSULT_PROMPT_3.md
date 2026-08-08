# Third consultation: calibration results and the main-run grid (post-freeze, pre-main-run)

You are being consulted as one of the two registered parties (Fable / Sol)
to the frozen "Neutral-Choice Randomization Experiment (Rung 1)".

Status: the design is frozen and published (manifest
ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040; repo
public at github.com/noahogbi/thus-therefore). The Phase 2 depth-calibration
pilot has run per SPEC section 7 — NATIVE GREEDY ONLY. No intervention has
ever been executed; no registered observable has been touched. Grid
selection from calibration is the frozen procedure; this consultation exists
because the calibration outcome is starker than the design anticipated and
one response option crosses the amendment line.

## Calibration pilot data (Qwen/Qwen2.5-7B base, frozen prompt format, greedy, n=40/cell, seed 1337)

| family:depth | with-trace acc | without-trace acc | gap |
|---|---|---|---|
| multiplication:2 | 0.550 | 0.350 | 0.200 |
| multiplication:4 | 0.075 | 0.000 | 0.075 |
| multiplication:6 | 0.000 | 0.000 | 0.000 |
| multiplication:8 | 0.000 | 0.000 | 0.000 |
| multiplication:10 | 0.000 | 0.000 | 0.000 |
| composition:2 | 0.250 | 0.000 | 0.250 |
| composition:4 | 0.100 | 0.000 | 0.100 |
| composition:6 | 0.075 | 0.000 | 0.075 |
| composition:8 | 0.050 | 0.000 | 0.050 |
| composition:10 | 0.000 | 0.000 | 0.000 |
| reachability:2 | 0.700 | 0.225 | 0.475 |
| reachability:4 | 0.650 | 0.375 | 0.275 |
| reachability:6 | 0.300 | 0.000 | 0.300 |
| reachability:8 | 0.175 | 0.000 | 0.175 |
| reachability:10 | 0.125 | 0.000 | 0.125 |

(n=40 -> roughly +/-8pp per cell. The no-trace condition appends a fixed
answer-immediately suffix to the frozen generator prompt; harness choice,
documented.)

## The issue

O1 is a destroyed-accuracy measurement: it needs cells where the model
actually succeeds WITH its trace. Two of three families are effectively
floored on this base model — composition never exceeds 0.25 even at its
easiest depth; multiplication is unusable past 2-digit operands. Only
reachability offers a real depth range with both headroom and large
with/without gaps. Consequence: the O2 depth axis would be carried
essentially by one task family, narrower than the design contemplated.

## Options — ruling requested, choose one

- **(3a) Proceed within the frozen design.** Main-run grid: reachability
  d2/d4/d6/d8 as the depth axis; multiplication:2 and composition:2 as
  secondary single-depth cells; floored cells reported per the frozen
  density-and-power policy. No amendment; grid selection from calibration
  is what SPEC section 7 prescribes. Also rule n per cell: 200 (SE ~3.2pp
  at p=0.3) or 400 (SE ~2.3pp) — cost difference is small ($40-70 vs
  $80-140 total across the ruled 25-pass arm plan).
- **(3b) Amend the model pin to a light-instruct checkpoint** (proposed:
  Qwen/Qwen2.5-7B-Instruct at a pinned revision), expected to lift
  with-trace accuracy across all families and restore a multi-family depth
  axis. This crosses the amendment line: environment.json is hashed, so it
  requires both parties' consent, a new manifest, a logged supersession,
  and a calibration rerun. Registration note for your consideration: SPEC
  section 6 wording covers "base and light-instruct checkpoints" for the
  zero-interaction registration, so an instruct pin arguably stays within
  the registered domain — but that reading is yours to make, not the
  implementer's. Timing note: no intervention data exists and the forum
  post is not yet published, so an amendment now is as clean as it will
  ever be.
- **(3c) Both, sequenced:** run 3a now (cheap, within-protocol, establishes
  the rung 1 floor on a true base checkpoint), and treat a light-instruct
  run as a pre-registered follow-on variation to be specified after 3a
  completes. If chosen, also rule the 3a n-per-cell.

## Response format

Reply with a single ruling (3a / 3b / 3c) plus the n-per-cell if
applicable, and the exact model+revision pin if 3b. Fable's standing
conservative tiebreak governs reconciliation of any disagreement. Anything
not ruled on remains frozen as-is.
