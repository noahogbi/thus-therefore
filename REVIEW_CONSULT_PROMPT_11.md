# Eleventh relay — corrected results, prediction scoring, and next steps (2026-08-21)

You are one of the two parties (Fable / Sol). The 10B rulings executed
cleanly: certification passed under the frozen epsilon (6.48M tokens
teacher-forced; 99.8%+ exact argmax; 13 exceedances, all diagnosed as a
canonical-tokenization instrument artifact appearing identically in
untouched control data; per the merged protocol 1 resumed record was
replaced by a certified regeneration and 2 were excluded with published
tally — exceedance_outcome_*.json). Corrected datasets are sealed
(sha256 in followon-instruct/corrected-dataset.sha256). The embargo is
lifted per the tenth-relay sequence. Below are the registered reads,
computed under the ninth-relay hierarchy, unchanged. The implementer
offers no interpretation; scoring your own registrations is yours.

## Registered O1 (mean accuracy penalty, native − randomized, pooled seeds)

Corrected data, both rungs. Rung 1's previously reported +0.055 aggregate
was the terminal-pass artifact; corrected values below.

| arm (interventions r1 / f-on) | RUNG 1 (base) | FOLLOW-ON (instruct) |
|---|---|---|
| Tier A aggregate (1,981 / 7,762) | **+0.012** | **+0.009** |
| connectives (245 / 5,721) | +0.000 | −0.000 |
| punctuation (547 / 1,197) | −0.005 | +0.002 |
| contractions (158 / 198) | +0.000 | −0.002 |
| whitespace (510 / 484) | +0.008 | +0.002 |
| operator spacing (483 / 52) | +0.002 | +0.002 |
| list markers (10 / 1) | +0.003 | +0.009 |
| discourse markers (0 / 0) | structurally unavailable | structurally unavailable |

Cell detail worth having: rung 1 aggregate is concentrated in
reachability:d2 (+0.045, the shallowest cell; penalties decline with
depth); whitespace multiplication:d2 is +0.016 corrected (was +0.211 under
the artifact). Follow-on aggregate's largest cells are reachability d6/d8
(+0.028/+0.031), d10 is −0.010.

## Registered O2 (depth interaction; primary = paired d4→d8 restricted slope)

| read | RUNG 1 | FOLLOW-ON |
|---|---|---|
| primary d4→d8, pooled | −0.001 | +0.007 |
| per seed | −0.001 / −0.001 / −0.002 | +0.006 / +0.008 / +0.007 |
| full reachability axis (secondary) | −0.006 | +0.000 |
| Proposal A arm×depth (supplementary) | +0.027 | +0.003 |

Reminder of standing context: rung 1's O2 was pre-declared
non-discriminating by both parties (sixth relay); the follow-on's primary
read was designated by the third consultation and carried through the
ninth-relay hierarchy.

## S1 / exposure (follow-on; rung 1 figures unchanged from RESULTS.md)

Aggregate intervened-site rate 2.45% of 620,144 candidate sites — 0.98×
rung 1's 2.5% baseline. Exposure redistributed rather than expanded:
connectives ~20% per-arm intervention rate; discourse markers 0
interventions across all seeds (265 candidate sites, none with ≥2 eligible);
list markers 1 intervention in 118k candidate sites. Per-arm table in
runs/corrected/chop_census_followon.json companion files.

## The registrations on the table (quoted forms; score your own)

- Sol (SPEC §6): positive depth interaction on the Tier A aggregate —
  penalty grows with required serial depth.
- Fable (SPEC §6): depth interaction ~zero for every rule on
  base/light-instruct checkpoints; ordering sub-prediction applies only to
  outcome-filtered checkpoints (not run here).
- Fable (ninth relay): aggregate intervened-site rate at least 2× base's
  2.5%, under 15% — realized 0.98×.
- Fable (ninth relay): in powered necessity cells (composition:4,
  reachability d6→d10), per-rule O1s within noise of zero excluding
  termination-mechanism effects; explicit "I lose cleanly" clause if a
  real unexplained penalty appeared there.
- Both parties' termination predictions: VOIDED WITH CAUSE (tenth relay
  10.2) — not scored.

## Questions

**(11.1) Score your registrations.** State, in your own words and against
the quoted forms, which of your registered predictions stand and which
fall on the corrected data, for each rung. Where you claim a stand, state
the numerical basis; where you concede a fall, say so plainly. Your
counterpart does the same; the reconciliation prints both verbatim in the
results document.

**(11.2) Supplementary proposals (IDEAS_FOR_NEXT_PREREGISTRATION.md).**
Bless, amend, or decline, severally:
  (a) watermark-capacity report from the native exposure data (free,
      descriptive);
  (b) trace-position decomposition of interventions incl. distance-to-end
      (free, descriptive);
  (c) real-watermark bridge arm: same 8-cell grid, native vs. published
      watermark schemes at standard strength (~$30, new generation,
      clearly labeled exploratory, never pooled with registered
      observables).

**(11.3) Publication.** The prereg post and results post publish together
per Noah's standing choice. The rung 1 correction notice and determinism
qualification are already applied to RESULTS.md with your approved
language. State any REQUIRED elements for the results post beyond what is
already ruled (the methods-lessons section will carry the terminal-pass
defect, the audit blind spot, the determinism finding, and the
attribution notes as logged).

Answer 11.1–11.3. Your counterpart receives this identical prompt;
reconciliation follows.
