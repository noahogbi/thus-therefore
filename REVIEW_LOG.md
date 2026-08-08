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
