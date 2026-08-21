# REVIEW_LOG — pre-freeze review dispositions (2026-08-07)

Record required by CLAUDE.md checkpoint Step 3. Findings F1–F5 were raised in
REVIEW_CONSULT_PROMPT.md (committed 2026-08-07) and ruled on by both registered
parties. Full party responses are preserved in the project conversation; the
operative rulings and what was applied are recorded here. Standing tiebreak
supplied by Fable: where rulings differ, adopt the more conservative option
(the one that randomizes less).

## F1 — Rule 03 sequencing set (dead code masking a conditional-Then trap)

- Fable ruled (1c): delete the sequencing set from the rule 03 table.
- Sol ruled (1a): accept as dead, explicitly "No table change"; record the set
  as structurally unavailable (density = 0), never to be interpreted as an
  observed zero penalty.
- **Reconciliation:** both rulings produce identical randomization (zero
  sequencing sites ever), so the tiebreak does not discriminate. A table
  amendment requires both parties' consent; Sol withheld it. APPLIED: table
  untouched; the matcher now skips the sequencing set explicitly in code (it
  previously died only via rule 02 overlap, which left rare edge cases — e.g.
  sentence-initial "Then, that ..." where rule 02's conservative guard skips —
  in which a sequencing site could have fired). Analysis must report the set
  as structurally unavailable, not as observed zero.

## F2 — Rule 02 display-line member swallowing rule 06 sites

- Both parties ruled (2b): amend. Fable (who drafted the original member and
  called it a drafting error) proposed members [".", ""]; Sol proposed
  members [".<linebreak>", "<linebreak>"] with the site anchored at the
  terminal-period position and including the existing line terminator, EOF
  lines without a trailing line break conservatively skipped.
- **Reconciliation:** Sol's wording adopted (per the tiebreak — it skips the
  EOF case Fable's version would allow — and because the empty-string member
  in Fable's version has no forced continuation, leaving the frozen raw-logP
  eligibility rule degenerate). Fable's clause "Interior operators remain
  eligible for rule 06" retained in the note.
- APPLIED: `rules/tier_a/02_punctuation.json` second candidate set replaced
  verbatim (see file); matcher updated to match.
- **Recorded mechanical consequence:** the amended span includes the display
  line's terminal newline, so where a display line is followed by a blank
  line, rule 02 now wins the overlap against rule 05's `\n\n` site at that
  boundary (02 < 05). Smaller footprint than the pre-amendment whole-line
  span, but nonzero; reported density will reflect it.

## F3 — Judge pin

- Fable: confirmed claude-sonnet-4-5-20250929 conditional on Sol's consent;
  pre-accepted a substitution by Sol sight unseen.
- Sol: rejected the Sonnet pin; ruled judge = **claude-opus-4-5-20251101**,
  temperature 0, thinking omitted/not enabled; one exact-request smoke test
  must pass before hashing; if unavailable, amendment protocol — no silent
  substitution.
- **Reconciliation:** Sol's pin adopted (strictly more capable, equally dated
  and pinned, satisfies temperature 0 with thinking off; chosen by the
  counterparty to the drafting lineage, which addresses Fable's own lineage
  rider more strongly than the original proposal). Fable's rider retained:
  audit runs immediately after the main generation run, before outcome
  analysis.
- APPLIED: environment.json updated (still DRAFT until checkpoint Step 4).
  PENDING before hash: the exact-request smoke test.

## F4 — Conservative matcher skips

- Both parties confirmed all three (whitespace \n\n-only; digit–digit minus
  excluded; rule 01 verb whitelist with no post-dry-run broadening).
- Fable's addition (code/reporting only): log matched-then-skipped counts per
  skip reason for rule 01, so analysis can report effective power on the rule
  both registrations lean on.
- APPLIED: matcher exposes per-reason rule 01 skip statistics
  (`match_sites_with_stats`); the dry-run report includes them.

## F5 — Rule 06 span semantics for eligibility scoring

- Both parties confirmed the substantive point: eligibility (Δ = 1.5) is
  scored over the operand-inclusive candidate span exactly as the table
  members are written, from the prefix immediately before <lhs>.
- They differed on bookkeeping: Fable confirmed the implementer's proposal to
  extend the matcher span; Sol rejected the extension because operand-
  inclusive spans of adjacent operators in one expression overlap on shared
  operands, and overlap resolution would then suppress sites arbitrarily — an
  unintended density artifact.
- **Reconciliation:** Sol's two-region design adopted: `edit_span` (operator
  plus its changed whitespace) drives replacement and overlap resolution —
  identical to the behavior both parties reviewed in the dry run — and
  `score_span` (operand-inclusive) drives eligibility scoring. NOTE: a strict
  reading of Fable's randomize-less tiebreak would pick the naive extension
  (it yields fewer sites via adjacent-operator suppression); it was not
  applied because the suppression is an accounting artifact unrelated to
  contamination risk, both parties agree on the scoring semantics, and the
  adopted design changes nothing about which sites randomize relative to the
  reviewed dry run. Flagged for Fable; may be revisited before hash.
- APPLIED: Site records `score_start`/`score_end`; for rule 06 they span
  <lhs> through <rhs>; for all other rules they equal the edit span.

## Implementation note IN-1 (2026-08-07, decoder build) — flagged for parties, not yet ruled

Building the intervention decoder surfaced a temporal-knowledge gap in one
frozen exclusion: rule 03's initiation set is dropped "whenever the trace
contains explicit ordinal enumeration" — a TRACE-GLOBAL condition. During
generation, the decoder must decide a site using only the text that exists at
that moment; an ordinal ("Second, ...") produced LATER would retroactively
flip the exclusion, and by then a randomized "First," -> "To start," would
already have broken enumeration parallelism (channel 2 — the hunt list's own
example). Per CLAUDE.md rule 2 (ambiguity -> skip), the decoder never
randomizes the initiation set mid-generation; such sites are logged with
skip_reason "global_exclusion_undecidable_mid_generation" and must be
reported as structurally unavailable during generation, mirroring the F1
treatment of the sequencing set. Table untouched. This is a mechanical
consequence of the frozen table's global wording plus causal decoding; the
parties should be shown this note before hashing. If they prefer a different
resolution (e.g., decide on trace-so-far), that is a pre-hash amendment
discussion.

## Second consultation reconciliation (2026-08-08) — IN-1 and arm plan

Both parties ruled on REVIEW_CONSULT_PROMPT_2.md; full responses preserved
in the project conversation.

- **IN-1: both ruled IN-1a** — the decoder's conservative skip of the
  initiation set during generation is confirmed; generation-time density is
  a structural zero, never evidence of a null; table untouched. Fable's
  logging addition APPLIED: skipped-site counts by reason are exposed
  (DecodeResult.skip_counts) so the writeup can state the density cost.
- **Arm plan: both ruled 2b with 3 intervention seeds per randomized arm** —
  native control + Tier A aggregate arm + all seven per-rule arms; the
  aggregate arm is the primary test of the section 6 aggregate predictions,
  per-rule arms are the registered per-rule decomposition and are never
  selectively promoted post hoc. Same three seeds across every arm (Sol).
- **Seeds:** audit_sample_seed = 314159 (both). Intervention seeds per
  Sol's ruling, unopposed by Fable: [271828, 161803, 141421] (digits of e,
  phi, sqrt(2) — nothing-up-my-sleeve). seeds.json field renamed to the
  plural intervention_sampling_seeds to carry the list; the file was
  fill-before-freeze by design.
- **Judge pin consent (Fable's record item):** Sol's consent to
  claude-opus-4-5-20251101 is Sol's own F3 ruling, which named that exact
  snapshot; Fable's consent given in the second-round reply. Both consents
  are hereby logged. Smoke test evidence: JUDGE_SMOKE_TEST.json.

With this, every party-level item is closed. Standing rule honored: nothing
further proposed that does not change a predicted observable.

## MANIFEST NOTE (2026-08-08) — canonical hash superseded pre-run

The manifest hash first committed (347cec05bd3f13567eb160a47ca0009c
a4d69b8c9a401f00bcce5509c9406d9f) was generated on Windows, where the
non-frozen tooling script hash_commit.py built its file map with
OS-native path separators. On the Linux experiment box the same frozen
content produced different map KEYS (rules/tier_a/... vs rules\tier_a\...)
and therefore a different aggregate hash. Verified before any fix: **all 14
per-file SHA-256 hashes were byte-identical across platforms** — the frozen
content never differed; only the bookkeeping keys did.

Resolution: hash_commit.py (tooling — deliberately absent from every frozen-
artifact list) now normalizes manifest keys to POSIX separators. Both
platforms now independently produce the canonical manifest hash:

  ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040

No frozen artifact changed (provable: identical per-file hashes in both
manifests, before and after — see git history for the superseded file).
Timing: before any generation run and before the forum post; the public
git history preserves the superseded manifest transparently.

## Third consultation reconciliation (2026-08-08) — calibration outcome and main-run grid

Both parties ruled on REVIEW_CONSULT_PROMPT_3.md; full responses preserved
in the project conversation.

- **Unanimous: 3c with n = 400 per cell.** The frozen base-model run
  proceeds on the calibration-selected grid; no amendment. Main-run grid:
  reachability d2/d4/d6/d8 (primary depth axis), multiplication:2 and
  composition:2 (secondary single-depth cells). Floored cells reported
  under the frozen density/power policy and never recruited into the depth
  regression.
- **Pre-data analysis commitments (recorded verbatim in intent, before any
  intervention data):** (1) Sol — the O2 estimate is described as "the
  depth interaction within the calibrated reachability family," with
  multiplication and composition as single-depth secondary checks; a
  positive reachability slope supports the registered prediction on this
  family and does not establish cross-family scaling. (2) Fable — d2/d4
  have nonzero without-trace accuracy (0.225, 0.375), so CoT-necessity is
  only partial there; O2 is read primarily from the d4->d8 slope;
  cross-family generalization claims are out of scope for this run.
  (3) Fable — the composition/multiplication floors are reportable
  findings for the calibration section (where the workspace regime begins
  at 7B scale), not discards.
- **Fable's tightening, adopted under the standing tiebreak:** the
  light-instruct follow-on is pre-registered NOW (FOLLOWON_INSTRUCT.md) —
  model pin Qwen/Qwen2.5-7B-Instruct @
  a09a35458c702b33eeacc393d103063234e8bc28, identified and logged before
  the base main run begins; identical procedure; own calibration and
  manifest; only execution gated on rung 1 completion. This executes Sol's
  follow-on proposal with the design-after-data door closed; strictly more
  binding on design freedom, overriding nothing Sol ruled. Flag to Sol as
  FYI in the next relay.
- **Implementation allocation (logged):** main-run problem generation uses
  frozen task seed 2026 (calibration used 1337), so the main-run problem
  stream does not overlap the calibration pilot's.

## Fourth relay reconciliation (2026-08-08) — partial; fifth relay issued

- **Item 1 (follow-on tightening): CLOSED.** No objection from either
  party. FOLLOWON_INSTRUCT.md stands as committed.
- **S1 (exposure reporting): ADOPTED, double consent.** Sol's wording
  governs: mean/median/distribution of realized intervened-site counts per
  (family, depth, arm), published beside frozen density, descriptive only,
  never a denominator for primary estimands. Fable consented to curve 1
  "under either version."
- **Curve 2: no jointly-consented definition.** Parallel replies: Sol
  declined the implementer's ratio (post-treatment conditioning — realized
  intervention count is downstream of treatment) and substituted a
  native-path exposure-adjusted regression; Fable consented to the ratio
  while disclosing a saturation bias in it favoring Fable's own side
  (bounded penalty + growing site count mechanically shrinks the ratio at
  depth) and offered a per-site survival hazard conditional on Sol's
  independent acceptance. Process note for the writeup: the two parties
  independently identified two DISTINCT flaws in the implementer's
  proposal, one of which the disclosing party flagged against its own
  interest.
- **Disposition:** REVIEW_CONSULT_PROMPT_5.md issued — one final binary
  cross-show round (ACCEPT/REJECT on each verbatim proposal; either party
  may answer DROP to invoke the fourth relay's pre-declared default
  immediately; no modifications by anyone). Any proposal with two ACCEPTs
  is adopted as supplementary; otherwise curve 2 is dropped permanently.

## Fifth relay reconciliation (2026-08-08) — CLOSED; consultation program complete

Binary round results: Fable "A: ACCEPT; B: REJECT"; Sol "A: ACCEPT;
B: REJECT".

- **Proposal A (Sol's native-path exposure-adjusted model): ADOPTED** with
  double consent, verbatim as circulated, including the native-vs-realized
  divergence publication clause. Supplementary; frozen O1/O2 primary.
- **Proposal B: dead by double rejection** — including its author's. Fable's
  non-binding rationale (recorded): B's k-bar is a realized randomized-arm
  quantity, post-treatment in exactly the way Sol's original objection
  targeted; A recovers per-intervention sensitivity without the endogeneity.
- Implemented: harness/exposure.py (native_eligible_counts with the IN-1
  initiation-set exclusion; S1 exposure stats; pure-python IRLS logistic
  with documented 1e-6 ridge; Proposal A design builder). 122 tests pass.
- Process note for the writeup: across relays four and five the parties
  independently identified two distinct flaws in the implementer's original
  proposal (post-treatment conditioning; saturation bias disclosed against
  the discloser's side), and one party rejected its own replacement on the
  merits after a no-advocacy cross-show. The supplementary analysis that
  survived is stronger than any single participant's first proposal.

No party-level questions remain open. Launch gates: credit top-up only.

## Rung 1 base run: executed, audited (2026-08-10/11)

- **Main run complete** under manifest ebb6bca0: 25 passes (native +
  aggregate + 7 per-rule arms x 3 seeds) x 6 ruled cells x n=400 = 60,000
  generations; every pass exactly 2400 records. Raw dataset committed
  (runs-raw-dataset.tar.gz).
- **Frozen audit PASSED:** 500 blinded pairs, seed 314159, judge
  claude-opus-4-5-20251101 @ temperature 0, thinking omitted. 500/500 PASS;
  every rule 100%; none below the frozen 98% threshold. No rule removed, no
  rerun triggered. Trail committed (audit_items / audit_key /
  audit_verdicts).
- **Measured exposure (S1):** 155,166 sites decided, 3,860 intervened
  (2.5%); 147,593 skipped as fewer_than_two_eligible. Per-cell coverage
  11%-40% of problems; exposure DECLINES with depth (reachability d2 ~24%
  -> d8 ~11%), inverting the confound that motivated the fourth-relay
  supplement. Discourse markers: 0 interventions run-wide. List markers:
  17.
- **Power consequence recorded before any outcome computation:** at
  reachability:d8, coverage and native accuracy bound the maximum possible
  penalty near 2pp against ~1.9pp sampling SE, so the d4->d8 slope (Fable's
  pre-committed primary O2 read) cannot resolve an effect of any size.
- **REVIEW_CONSULT_PROMPT_6.md issued** asking both parties to rule, BLIND
  to any outcome number, on how O2 should be reported (6a report as frozen
  / 6b report plus pre-declared non-discrimination / 6c other). No O1, O2,
  or per-arm accuracy has been computed by anyone, including the
  implementer; harness.analysis has not been run.

## Sixth relay — Sol ruling received 2026-08-11 (Fable pending)

**Sol: 6b** — compute and publish O1/O2 exactly as registered, per rule and
aggregate, with frozen density/power reporting and the Proposal A exposure
adjustment; do NOT alter cells, estimands, or analysis because of measured
exposure. Registered interpretation, recorded before outcomes exist:

- The base-model O2 result is **non-discriminating** between the parties'
  registered depth-interaction hypotheses. Neither the sign nor the
  statistical significance of the O2 estimate will be claimed by Sol as
  evidence for or against either prediction. O2 is published because it is
  a registered observable, as an underpowered secondary result.
- The non-discrimination ruling does **not** extend automatically to O1 at
  better-exposed cells, nor to descriptive/mechanistic findings; those are
  interpreted according to their own measured power.
- **Zero observed penalty is not evidence of invariance when intervention
  opportunity is near zero.** Rule 03 has no experimental O1/O2 estimate at
  all — zero interventions means structurally unavailable, not a null
  effect. Rule 07 is to be described as effectively uninformative rather
  than as meaningful evidence from 17 interventions.

Non-binding: Sol reports the measured exposure materially increases the
light-instruct follow-on's priority, which now answers two distinct
questions — (1) whether stronger instruction tuning yields enough
reader-equivalent choice entropy for the instrument to have power, and
(2) whether neutral-choice dependence changes relative to the base
checkpoint.

**Fable: 6b** — same disposition, invoked explicitly against Fable's own
side. Recorded reasoning: an underpowered O2 spuriously flatters the flat
registration; at ~11% coverage and 0.175 native accuracy a 2pp maximum
detectable effect against 1.9pp SE cannot distinguish flat from positive at
any effect size either party contemplated, so 6a would position Fable to
claim confirmation from data constitutionally incapable of disconfirming
it. Fable pre-commits never to cite this run's O2 as support for the flat
prediction.

Additional Fable contributions, stated blind and pre-outcome:

- **Substantive finding for the writeup:** 95% of decided sites had fewer
  than two eligible alternatives under Delta = 1.5. On this base model the
  reader-neutral channel is mostly **closed at the writer** — the surface-
  form distribution is too peaked to offer comparable alternatives. This is
  a measured property of the contested channel (its available write
  capacity), independent of whether anything uses it, and belongs beside
  the audit result.
- **Auxiliary assumption falsified, recorded pre-outcome:** Fable predicted
  discourse markers would be a high-density, high-entropy rule; the rule
  produced 12 sites and zero interventions. The post-RL ordering
  sub-prediction keeps its logic (effects concentrate where entropy exists)
  but its rule ranking must be read against measured rather than assumed
  entropy.

**RECONCILIATION: 6b unanimous.** O1/O2 computed and published exactly as
registered, per rule and aggregate, with frozen density/power reporting and
the Proposal A exposure adjustment; no cells, estimands, or analyses
altered on account of measured exposure. Both parties' non-discrimination
statements bind: this run's O2 is evidence for neither registration. Sol's
qualifiers carry: the statement covers O2 only (O1 at better-exposed cells
and descriptive findings are read on their own power); rule 03 is
structurally unavailable rather than a null; rule 07 is uninformative
rather than evidence.

**Follow-on (both, non-binding, concordant):** priority rises
substantially. Fable's framing — the exposure finding converts the
light-instruct follow-on from robustness check into the experiment's crux,
since both stories route through whether post-training OPENS the writer
(Fable: channel stays near-closed until outcome-filtered selection builds
an encoder; substrate story: capacity is cheap to open and gets used). Sol
concurs the follow-on now answers two questions: whether instruct tuning
yields enough reader-equivalent entropy for the instrument to have power,
and whether neutral-choice dependence changes. Both name the RLVR-stage
comparison as the decisive third point. No design changes needed — density
and exposure reporting are already frozen in.

## Rung 1 analysis computed (2026-08-11) — seventh relay issued

Computed under the unanimous 6b ruling; no cell, estimand, or analysis
altered on account of measured exposure.

- **O1 pooled across seeds:** aggregate +0.055; whitespace +0.043;
  connectives +0.007; operator spacing +0.002; contractions +0.000;
  punctuation -0.005; list markers +0.003 (uninformative); discourse
  markers structurally unavailable. Seed consistency tight (+0.055,
  +0.051, +0.058 aggregate).
- **O2 reachability:** aggregate slope -0.009; restricted d4->d8 -0.0004;
  per-rule slopes within +/-0.005. Published as underpowered secondaries;
  claimed by neither party per their pre-declared statements.
- **Mechanism finding:** the aggregate O1 is almost entirely rule-05
  whitespace interventions in multiplication:d2 (+0.211, z ~ 7.4, all
  three seeds). Decomposition: of 126 touched traces, 122 produced no
  parseable ANSWER and stopped early on EOS (mean 88 tokens vs 142
  untouched; native no-answer rate 2.5%). The penalty is generation
  TERMINATION, not degraded arithmetic: swapping `\n\n` for `\n` at an
  existing paragraph boundary removes a continuation cue in this base
  model.
- **Audit blind spot recorded:** rule 05 passed the frozen audit at 100%
  on 130 items and was correct to — the five criteria judge excerpt
  meaning, not downstream continuation. Discoverable only by running the
  experiment.
- **REVIEW_CONSULT_PROMPT_7.md issued** requesting rulings on reporting of
  the rule-05/aggregate O1, a supplementary wrong-number vs no-answer
  decomposition, framing of the termination dependence, whether the audit
  blind spot is recorded for future pre-registration, and a non-binding
  follow-on question. No frozen estimand is altered by any option; nothing
  is written up as a claim pending reconciliation.

## Seventh relay reconciliation (2026-08-11) — rung 1 reporting settled

- **7.1 — unanimous (d) = b and c jointly.** Publish the frozen raw O1 as
  computed; the termination decomposition is a REQUIRED companion; a
  supplementary aggregate excluding rule 05 appears additionally, labeled a
  mechanistic decomposition and never a substitute. Sol's required framing
  language adopted verbatim in RESULTS.md. Implementation note: the
  exclusion aggregate is computed from the independent per-rule arms rather
  than by subsetting the aggregate arm on which rules fired, which would be
  post-treatment conditioning of the kind Sol objected to in relay four.
- **7.2 — unanimous consent; Sol's three-way form adopted** (correct /
  wrong parseable answer / no parseable answer) per arm and cell, as a
  superset of Fable's two-way split. Frozen O1 unchanged: no-answer traces
  remain incorrect.
- **7.3 — unanimous (b):** distinct phenomenon, reported separately;
  both parties explicitly declined (c) artifact. Names offered: Fable
  "termination-cue sensitivity"; Sol "reader-neutral continuation-state
  dependence". Both recorded; both quoted in RESULTS.md.
- **7.4 — consent to recording the blind spot is unanimous; the proposed
  REMEDY is disputed.** Fable: add a behavioral continuation check
  (P(EOS)/next-token divergence profiling) at table-validation time. Sol:
  rejects that as a neutrality gate — "excluding transformations whenever
  they affect continuation would condition the instrument on the causal
  outcome it is designed to detect" — and proposes instead extending the
  READER-side audit to document-state equivalence (does a competent reader
  regard the swap as changing apparent completion status / block boundary /
  expectation of further text), with model-continuation testing permitted
  DIAGNOSTICALLY only. Partial convergence recorded: both permit
  continuation profiling as a diagnostic; they differ only on whether it
  may gate neutrality. Disposition: the blind spot is recorded as
  unanimous; both remedies are recorded with attribution as an open
  question for the NEXT pre-registration. This affects no rung 1 reporting,
  and the standing conservative tiebreak is not invoked because the dispute
  is about validity rather than degree of randomization.
- **7.5 — concordant pre-run registrations.** Fable: the multiplication:d2
  rule-05 termination effect collapses to near zero on the instruct
  checkpoint (residual under 2pp), with eligible-alternative density rising
  modestly. Sol: substantially smaller in instruct. Fable offered
  "termination sensitivity survives instruct tuning" as Sol's win condition
  for the substrate story; **Sol explicitly declined to tie it to the
  original covert-state disagreement**, keeping it a separate question.
  Recorded as offered-and-declined.

**Fable's recorded self-corrections (attributed, post-outcome but
volunteered):** (1) Fable's registered whitespace prediction ("zero on
base") is wrong as written — the registration allowed small constant
brittleness and located it on connectives, and +0.211 in a cell is not
small; logged as a miss with Fable's attribution. (2) Delta-eligibility
passed both whitespace forms as comparable — the model rated `\n` a
near-equivalent continuation and then treated its own alternative as a stop
sign. Fable's formulation: eligibility certifies write-side plausibility,
not read-side equivalence; that asymmetry is now empirical.

## Eighth relay reconciliation (2026-08-11) — unanimous 8.1(b), 8.2(b)

- **8.1(b) unanimous — minimal measurement-side amendment for the
  follow-on.** Fable's tightening adopted: the extended rule is frozen as
  exact mechanics with no judgment calls — extraction is the frozen
  ANSWER-line regex with precedence, else the LAST \boxed{<integer>} in the
  trace, nothing else accepted; terminal set is exactly {configured chat
  EOS, literal <|endoftext|>}. Prompt bytes unchanged (raw generator text,
  no chat template) preserving the byte-identical paired comparison. New
  follow-on manifest to be cut with the rule recorded under the hash;
  recalibration before any main-run data.
- **8.2(b) unanimous — rung 1 dual-report.** Frozen numbers primary and
  untouched; supplementary full re-extraction under the identical extended
  rule (no rung-1-specific tuning), all affected O1/O2 recomputed and
  labeled supplementary. Sol's addition adopted: extraction transition
  counts published by (family, depth, arm). Fable's safety condition
  adopted: the recomputation script commits BEFORE it runs. Fable's
  extension recorded: if flips prove arm-imbalanced enough to move O1/O2
  materially, that is a reportable measurement-sensitivity finding, and the
  sixth-relay non-discrimination statement extends to the supplementary O2
  automatically.
- **8.3 — predictions restated/reaffirmed pre-recalibration.** Fable,
  falsifiable forms: (i) instruct multiplication:d2 rule-05 termination
  differential (touched -> no-parseable-answer rate) falls below 2pp,
  termination meaning any token in the frozen terminal set; (ii) aggregate
  intervened-site rate at least doubles from base 2.5% while remaining
  under 15%; win-condition offer to Sol stands at >= 5pp surviving
  termination sensitivity. Sol: prediction unchanged (substantially smaller
  termination effect), with the required distinction that reduced
  rule-05-induced premature termination supports the prediction while
  eliminating post-answer runaway is a harness repair and is not evidence.
- **Watch item (Fable):** if the reachability:d4 with<without inversion
  (-0.30) survives the 8.1(b) recalibration, it stops being a format
  artifact and requires attention.
- **Writeup finding (Fable):** the frozen without-trace condition scored
  0.800 because it was an instruction-following test — calibration
  protocols themselves do not transport across training stages; directly
  relevant to the future RLVR-stage comparison.

## Follow-on recalibration under 8.1(b) (2026-08-12)

Rerun on the frozen pin under manifest 5bcf4dc8, prompt bytes unchanged
(grid: followon-instruct/calibration-instruct-8_1b.json). The transport
failure was measurement-side in its entirety: multiplication:d2 with-trace
0.050 -> 1.000. Fable's watch item resolved — the reachability:d4 inversion
(-0.30) did not survive the amendment (+0.05, format artifact); what
remains real is weak CoT-necessity at d4 on this checkpoint (without-trace
0.675 vs base 0.375). Ninth relay (REVIEW_CONSULT_PROMPT_9.md) sent: one
ruling on the instruct main-run grid (rung 1's exact cells vs mechanical
re-selection vs union; drop-default (a)), plus non-binding reconfirmation
of the 8.3 predictions against the realized grid. Nothing runs until both
replies reconcile.

## Ninth relay reconciliation (2026-08-12) — unanimous 9.1(c), union grid

- **Grid: rung 1's six cells plus reachability:10 and composition:4, n=400
  per cell** (multiplication:2, composition:2, composition:4, reachability
  2/4/6/8/10). Both parties chose (c) independently.
- **Analysis hierarchy, frozen before any intervention data** (Fable's
  pre-commitment and Sol's pre-declaration are compatible; both adopted in
  full as the conservative union of constraints):
  1. PRIMARY O2 read — the paired d4->d8 restricted reachability slope,
     carried verbatim from the rung 1 commitment for cross-checkpoint
     comparability.
  2. SECONDARY — full d2->d10 reachability axis, labeled per-checkpoint;
     d4 flagged as weak-CoT-necessity (gap 0.050, without-trace 0.675).
  3. TERTIARY — composition:2->4 two-point cross-family consistency check,
     never pooled into the reachability slope.
  - Paired base->instruct comparison uses the ORIGINAL SIX cells only
    (Sol); reachability:10 and composition:4 are never retroactively added
    to any rung 1 analysis (Sol); composition:4 reported as supplementary
    evidence that the instruct checkpoint opens a region unavailable at
    base (Sol).
  - Ruled interpretive commitments, stated pre-run (Fable): a null at
    reachability:d4 is uninformative (cell barely needs its trace); the
    interesting paired contrast is d6/d8 where necessity is strong on both
    checkpoints.
- **9.2 predictions against the realized grid:** Fable — both falsifiable
  forms stand unchanged (mult:d2 touched->no-parseable-answer differential
  < 2pp under the frozen terminal set; aggregate intervened-site rate >=
  2x base's 2.5% and < 15%), PLUS a new pre-run registration enabled by
  the union grid: in the powered CoT-necessity cells (composition:4,
  reachability d6->d10), per-rule O1s remain within noise of zero
  excluding rule-05 termination-mechanism effects — the flat-interaction
  registration in its first honestly testable form; an unexplained real
  penalty in those cells is a clean loss, acknowledged in advance. Sol —
  comparative prediction unchanged (substantially reduced termination
  sensitivity vs rung 1); explicitly declines to add a numerical threshold
  after seeing calibration.

## Remaining before hash (checkpoint Step 4)

1. DONE 2026-08-08 — Noah's explicit sign-off on the reviewed site list
   (post-amendment dry run, 298 sites), given in-session: "Signed off."
   Checkpoint Step 4 gate cleared.
2. DONE 2026-08-08 — Judge smoke test passed (Sol's F3 condition): exact
   request served by claude-opus-4-5-20251101 at temperature 0, thinking
   off; well-formed PASS verdict returned. Evidence: JUDGE_SMOKE_TEST.json.
3. Show the parties IN-1 (decoder initiation-set rule) and settle the arm
   plan (all-rules aggregate and/or per-rule arms).
4. Fill seeds.json (intervention_sampling_seed, audit_sample_seed —
   proposed: 271828 and 314159, nothing-up-my-sleeve digits of e and pi).
5. Finalize environment.json (remove DRAFT status).
6. `python scripts/hash_commit.py`; commit the manifest.
7. Publication at freeze (adopted 2026-08-07): flip the repo public
   (`gh repo edit --visibility public`), then publish writeup/prereg_post.md
   with the manifest hash and repo URL filled in — BEFORE the first
   generation run, so the pre-registration is publicly timestamped.


## Tenth relay reconciliation — 2026-08-20 (decoder defect disposition)

Both parties ruled on REVIEW_CONSULT_PROMPT_10 (defect disclosure; outcome
numbers embargoed from both parties and from the prompt).

**10.1 — UNANIMOUS (d): deterministic resume-and-complete, both rungs.**
Merged preconditions, all adopted: automatic total per-rung fallback to full
rerun on a single RNG-replay or byte-identity failure (Fable i, Sol 4);
validation >=100/rung, stratified arm x cell, small strata whole, full
from-scratch regeneration, exact identity on all record fields (Sol 2-3,
supersedes Fable ii's 50); programmatic signature census of every
randomized record, published per cell (Fable iii -> chop_census_*.json:
followon 5,064 chopped of 12,070 touched; rung1 985 of 3,693); decoder
mutation-path regression audit (Fable iv -> DECODER_PATH_AUDIT.md);
freeze-before-execute with immutable originals and per-record provenance
(Sol 1 -> REPAIR_PLAN.md); publish resumed counts + validation summary
(Sol 5). Corrected data is primary for both rungs; as-run randomized data
is superseded history retained with the defect notice (Fable).

**10.2 — UNANIMOUS: termination registrations voided-with-cause, both
parties, not resurrected.** Sol's rung 1 correction text adopted as the
substance of the RESULTS.md notice. Fable's three required elements
adopted: (1) explicit self-attributed retraction of the 7.3(b)
interpretation ("the contested channel exists and its first observed cargo
was formatting" — a claim about a decoder bug); (2) 7.4's audit-blind-spot
observation stands as design insight, its motivating instance flagged as
artifact; (3) the P(EOS)-at-substitution probe that exposed the defect is
noted as the 7.4-proposed behavioral continuation check, recommended into
the next pre-registration's validation phase. Sol's addendum: the clean
audit remains valid — it certified substitution neutrality, not decoder
execution.

**10.3 — CONFIRMED with Fable's scoping addition.** Embargoed as-run
outcome files deleted unread by the parties (Sol: quarantine/delete).
Blinding scope logged for the writeup: party rulings were blind to all
outcome data; the implementer's defect diagnosis necessarily was not (the
anomaly was found in the analysis) — the writeup must state this precisely.
Fable's unprompted note is logged at Fable's request, for the limitations
section: relays 6-9's most confident interpretive writing was built on the
artifact, the audit passed the artifact because excerpt-level audits cannot
see continuation effects, and the mechanism-check-before-interpretation
ordering is the project's own lesson, failed locally by its proposer.

Sequence per Sol: reconcile (this entry) -> freeze repair (REPAIR_PLAN.md,
this commit) -> execute + validate -> fallback if any failure -> corrected
frozen analysis under the unchanged ninth-relay hierarchy -> results relay.


## Relay 10B reconciliation — 2026-08-21 (validation gate superseded)

**10B.1 — UNANIMOUS (i):** repair accepted under the demonstrably-external
clause; byte-identity gate formally superseded by an outcome-blind
greedy-consistency certification. Both parties independently found the
byte-exact criterion unsatisfiable by any procedure on the measured stack
(including the rerun fallback each had mandated); Fable notes its own
zero-tolerance clause "fired exactly as designed and thereby falsified its
own premise." Merged certification requirements, all adopted:
- epsilon frozen BEFORE certification, derived solely from the outcome-blind
  divergence-diagnosis margins (Sol), outliers (3.375, 6.75) not
  grandfathered (Fable a). FROZEN: epsilon = 2.0 logits — strictly above the
  observed ULP-scale mass (max 1.875), below the outlier gap (3.375).
- Certification of every resumed tail token: rank and logit deficit vs the
  contemporaneously recomputed argmax under teacher forcing; full
  distributions published, not pass/fail (Sol).
- Uniform application: matched-size random samples of native and
  untouched-randomized records certified identically, so greedy-consistency
  is a dataset property, not a repaired-record special (Fable b).
- Exact ties (deficit 0.000): argmax undefined; either branch is
  greedy-consistent; stack tie-break behavior documented (Fable c).
- Exceedance protocol (merged Fable a / Sol 3): an epsilon exceedance halts
  analysis and triggers diagnosis; idiosyncratic exceedances get one full
  from-scratch regeneration, which must itself pass certification or the
  record is excluded with a published tally; any systematic splice-local or
  RNG/state pattern fails the repair and returns to the parties before any
  outcome is examined. A rerun is recognized as not a cure for numerical
  nondeterminism.

**10B.2 — UNANIMOUS approve, scope cut precisely:**
- Input identity (task seeds, prompt bytes across checkpoints) is untouched
  and remains the paired-comparison foundation (Fable).
- Decoding determinism rescoped everywhere (rung 1 included): greedy, but
  bf16 inference with KV-cache reuse is empirically not byte-repeatable at
  near-tied argmax decisions; "bit-identical" claims stand only where
  identity was directly demonstrated for the specific replay discussed
  (Sol's qualification text adopted).
- "(a) computed lazily" retired; replaced by Sol's formulation: "a corrected
  continuation conditional on the realized prefix, rather than a
  byte-for-byte shortcut to a hypothetical full rerun." Attribution shared:
  implementer overclaimed, Fable endorsed and amplifies the retraction.
- Explicit statement required (Fable): the three-seed-per-arm design
  absorbs tie-flip noise into the reported seed-to-seed spread, so the
  finding affects determinism language, not the error structure of the
  registered estimates.
- Reported regardless of eventual O1/O2 (Sol): apparatus property found
  under outcome embargo, not post-hoc explanation.
- Methods-lessons (Fable, logged): second consecutive relay where the
  validation machinery's failure was the informative event — the
  terminal-pass defect exposed the audit's downstream blindness; the
  byte-identity gate exposed the determinism fiction the repo's own tooling
  had been asserting.

Sequence resumes per the tenth relay: certify -> publish margins -> unseal
corrected analysis under the unchanged ninth-relay hierarchy.


## Eleventh relay reconciliation — 2026-08-21 (results scored)

**11.1 — Both parties' self-scorings received; print verbatim in results
document (Fable 11.3(i), Sol requirement 1).** Summary of record:
- Fable: density registration FALLS (0.98x vs registered >=2x); per-rule
  flat STANDS both rungs (all informative arms within +/-0.005); rung 1 O2
  cited as nothing per its own blind non-discrimination commitment;
  follow-on aggregate registration "strained, not fallen" — final score
  CONDITIONED, stated before any decomposition ran: falls if (i) the
  11.2(b) position decomposition shows the aggregate d6/d8 penalty is not
  a late-trace mechanistic confound AND (ii) per-cell CIs exclude zero
  under the frozen analysis. Whitespace-miss concession of seventh relay
  retracted-with-cause. Outcome-filtered clause unrun, unscored.
- Sol: rung 1 UNRESOLVED by prior pre-outcome non-discrimination ruling
  (observed sign opposite its registration; declines both rescue and
  self-falsification per that ruling); follow-on registration STANDS on
  the pre-designated primary read (+0.007, seeds +0.006/+0.008/+0.007),
  claimed narrowly: supports registered sign on the primary contrast, does
  not establish monotonic depth law (full axis +0.000, Proposal A +0.003);
  termination voided, no score.
- Neither registered shape matched the follow-on data in full (Fable
  11.3(iii)): flat fails at aggregate d6/d8; monotone growth fails at d10.
  Super-additivity observation (aggregate penalty absent in the
  connectives-only arm carrying 74% of its interventions) recorded as
  DESCRIPTIVE and UNREGISTERED.

**11.2 — Supplements, merged rulings:**
(a) BLESSED with Sol's naming amendment: "available reader-neutral channel
    capacity proxy," never "watermark capacity"; report site fractions,
    eligible-set size distribution, log2(k) nominal bits, per-trace and
    per-token, distributions not just means; entropy-weighted variant
    separate if computed. Fable adds: connect to watermarking capacity
    assumptions in the writeup.
(b) BLESSED by both; PRIORITY (Fable: run before the results post is
    finalized; its own scoring is conditioned on it). Outcome-blind first
    report: opportunity and realized interventions vs normalized position,
    absolute token position, distance-to-termination, and
    before/within/after final reasoning step where identifiable. Any
    causal position claim is a separately labeled later analysis.
(c) BLESSED AS AMENDED by Sol: three arms (native / exposure-matched
    neutral randomization / published watermark at standard strength),
    with the full freeze list (scheme+version, strength, rule classes,
    payload, key/seed, detector+statistic, exposure-matching procedure)
    committed before generation. Exploratory, own manifest, never pooled.
    Fable frames it as pricing the semantic-equivalence-class enforcement
    question from the original exchange.

**11.3 — Results post required elements, union of both lists:** compact
prediction ledger without retroactive reinterpretation; primary and
secondary depth reads always shown together; corrected effect scale
prominent (the +0.055 artifact's rhetorical magnitude must not survive its
retraction); exposure-redistribution/channel-availability as HEADLINE
result (writer ~97.5% closed at Delta=1.5; 0.98x across checkpoints);
both 11.1 texts verbatim; super-additivity flagged unregistered; ladder
status explicit (rungs 2-4 unrun, outcome-filtered crux open — the
contribution is the certified instrument, the capacity measurement, and
priced-and-scored registrations, not resolution); methods-lessons
unsoftened including both validation-gate failures. Sol's restrained
top-line summary adopted as the candidate abstract.


### Eleventh relay — Fable's condition resolved (same day, outcome-blind side computed first)

11.2(b) decomposition and frozen per-cell CIs, as Fable's 11.1 conditioned:
(i) NO late-trace confound: aggregate d6/d8 interventions sit at 19-24% in
the final fifth of the trace (less end-concentrated than every other cell
class; composition/multiplication run 54-80%), median 435-519 tokens from
termination, 63-74% before the final answer step. (ii) Per-cell 95% CIs
INCLUDE zero: d6 +0.028 [-0.026,+0.083]; d8 +0.031 [-0.024,+0.086].
Per the condition's own terms the aggregate-flat registration is NOT
scored fallen; it remains "strained, not fallen" with both facts printed.
Capacity proxy (11.2(a), Sol's naming): sites with >=2 eligible are 4.6%
(follow-on) / 4.9% (rung 1) of candidate sites on the decode path; nominal
uniform-choice capacity 1.72 bits/trace mean (median 1.0) on instruct,
0.54 bits/trace (median 0.0; 53% of traces zero) on base; 2.6 / 1.5 bits
per 1000 generated tokens. Labeled proxy, not demonstrated end-to-end
capacity, per Sol's amendment.


### Relay 11B — final confirmations (2026-08-21). PUBLICATION CLEARED.

11B.1 final ledger lines received, both to print verbatim: Fable's
"strained, not fallen" text as supplied (registration "survives on
statistical power, not vindication"; unregistered shape acknowledged;
outcome-filtered crux unrun). Sol confirms with the appended refinement:
"directionally supported, not statistically resolved" — stands under the
literal preregistered sign criterion, not to be presented as strong
mechanism evidence; position data removes one confound, does not upgrade
evidentiary strength. 11B.2 both confirm publication with nothing further;
Fable verifies 11.3(iii) rides in the ledger; Sol's sentence to place
prominently: "Available neutral-choice capacity is not evidence that the
model actually uses that capacity to transmit hidden task state."
11B.3 bridge arm AFTER publication, unanimous; Fable's non-blocking freeze
suggestion recorded (capacity proxy under each watermark scheme's own
effective Delta for comparability). Fable's closing sentence logged at its
request, to close the ledger where it opened: "we set out to price a
disagreement, and the price list survived contact with two harness
defects, a determinism fiction, and both of our registered shapes being
wrong somewhere — which is, as far as I can tell, what it looks like when
the procedure is doing the work instead of the participants."
