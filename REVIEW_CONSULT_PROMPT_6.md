# Sixth relay: audit result, measured exposure, and how O2 should be reported

You are one of the two registered parties (Fable / Sol). The rung 1 base
main run is COMPLETE and the frozen audit has PASSED. This relay is sent
**before any outcome number has been computed** — no O1, no O2, no
per-arm accuracy, by anyone, including the implementer. The analysis code
has not been run. That is deliberate: the ruling requested below concerns
how a registered observable should be reported, and it must be made blind
to the value it takes.

## 1. Run completed as ruled

25 passes: native control + Tier A aggregate + seven per-rule arms, three
intervention seeds each, six ruled cells at n = 400. 60,000 generations,
every pass exactly 2,400 records. Manifest
ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040. Raw
dataset committed to the public repo.

## 2. Frozen audit: PASSED, cleanly

500 blinded excerpt pairs (audit seed 314159) judged by
claude-opus-4-5-20251101 at temperature 0, thinking omitted.

| rule | n | pass | rate |
|---|---|---|---|
| tier_a_01_connectives | 60 | 60 | 100% |
| tier_a_02_punctuation | 147 | 147 | 100% |
| tier_a_04_contractions | 42 | 42 | 100% |
| tier_a_05_whitespace | 130 | 130 | 100% |
| tier_a_06_operator_spacing | 119 | 119 | 100% |
| tier_a_07_list_markers | 2 | 2 | 100% |
| ALL | 500 | 500 | 100% |

Zero interventions were judged to alter propositions, dependency
structure, hedging, explicit-intermediate selection, or
schedule/granularity. No rule removed; no rerun triggered. The channel
isolation the design depends on is certified.

## 3. Measured exposure — the reason for this relay

Across all 24 randomized passes the harness decided 155,166 sites and
intervened on **3,860 (2.5%)**. 147,593 sites were skipped as
`fewer_than_two_eligible`: under the frozen Delta = 1.5 nats, this base
model rarely has two reader-equivalent surface forms it considers
comparable.

Per-rule totals (all passes):

| rule | sites decided | intervened |
|---|---|---|
| tier_a_01_connectives | 11,334 | 512 |
| tier_a_02_punctuation | 29,588 | 1,095 |
| tier_a_03_discourse_markers | 12 | **0** |
| tier_a_04_contractions | 5,973 | 334 |
| tier_a_05_whitespace | 17,439 | 935 |
| tier_a_06_operator_spacing | 46,121 | 967 |
| tier_a_07_list_markers | 44,699 | **17** |

Aggregate-arm coverage per cell (consistent across all three seeds):

| cell | problems touched | mean interventions/problem | native-path mean eligible |
|---|---|---|---|
| composition:d2 | ~40% | 0.41 | 0.90 |
| multiplication:d2 | ~36% | 0.36 | 0.69 |
| reachability:d2 | ~24% | 0.29 | 0.51 |
| reachability:d4 | ~23% | 0.26 | 0.47 |
| reachability:d6 | ~18% | 0.18 | 0.38 |
| reachability:d8 | **~11%** | **0.12** | 0.21 |

Three consequences, stated without interpretation:

- **Exposure DECLINES with depth**, inverting the confound that motivated
  the fourth-relay supplement. Deeper reachability problems receive fewer
  interventions, not more. (Proposal A remains valuable — it now adjusts
  for declining rather than growing exposure.)
- **Maximum detectable effect at the top of the depth grid.** At
  reachability:d8, coverage ~11% and native accuracy ~0.175 bound the
  largest possible penalty at roughly 2 percentage points even if EVERY
  intervention derailed its trace; sampling SE at n = 400 is ~1.9pp. The
  d4->d8 slope that Fable pre-committed as the primary O2 read therefore
  sits in a range where no effect of any size could be resolved.
- **Two rules are structurally unreportable.** Discourse markers produced
  zero interventions across the entire experiment (12 sites decided, all
  initiation-set, all skipped per IN-1; the attention and recap sets never
  matched these traces). List markers produced 17 across 24 passes, and
  contributed 2 of 500 audit items.

## 4. Ruling requested — how should O2 be reported from this run?

The frozen policy (SPEC section 9) already requires density and power to
be reported and forbids discarding a valid low-density run. The question
is what interpretive weight the O2 estimate carries, decided now, blind.

- **(6a) Report as frozen.** Compute and publish O1/O2 per rule and
  aggregate exactly as registered, with density and power alongside, and
  let readers weigh them. Pre-committed wording from the third
  consultation still applies.
- **(6b) Report as frozen, plus a pre-declared non-discrimination
  statement.** Same computation and publication, but both parties record
  NOW that this run's O2 is underpowered at the depth range that
  discriminates the registrations, and neither party will claim it as
  evidence for or against their prediction. The run's primary reportable
  results become the audit-certified instrument, the measured neutral-
  channel exposure, and the calibration findings; O2 is published as an
  underpowered secondary.
- **(6c) Other** — specify. Note that any option selecting cells by
  observed exposure AFTER seeing outcomes would be post-hoc cell
  selection; the implementer flags this as the one shape to avoid.

Please also indicate, non-bindingly: does the measured exposure change
your view of the pre-registered light-instruct follow-on's priority?

## Response format

Reply with 6a / 6b / 6c (plus wording if 6c), and the optional follow-on
note. Fable's standing conservative tiebreak governs reconciliation. On
receipt of both rulings the analysis will be computed and reported
accordingly — not before.
