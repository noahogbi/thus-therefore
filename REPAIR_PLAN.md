# REPAIR_PLAN.md — frozen repair procedure (tenth relay, unanimous 10.1(d))

Frozen per Sol's precondition 1 before any execution. The executing commit
is the one that adds this file; its hash is the procedure's identity (git
history is the audit trail). Original datasets are immutable inputs;
corrected datasets are new directories with per-record provenance.

## Ruling being executed

10.1(d): deterministic resume-and-complete of defect-affected records, both
rungs, with (merged preconditions):
- Programmatic defect-signature census of every randomized record, published
  (Fable iii): `runs/corrected/chop_census_{rung}.json`. Strict signature:
  trace ends exactly at the last intervened site's splice
  (len(text) == site.start + len(chosen)).
- Validation >= 100 records per rung, audit-seed selected
  ("repair-validation:314159:{rung}"), stratified arm x cell proportional to
  chop counts, small strata taken whole (Sol 2 ⊇ Fable ii). Realized:
  followon 122/71 strata, rung1 123/51 strata.
- Every validation record regenerated ENTIRELY from scratch via
  harness.runner.run_problems under the fixed decoder; exact identity
  required on text, generated_tokens, ended, sites, density,
  answer_extracted, correct (Sol 3).
- Zero tolerance: one RNG-replay mismatch or one non-identical validation
  record fails the method for that rung; automatic full randomized-arm rerun
  fallback (Fable i, Sol 4). No partial salvage.
- Decoder-path regression audit (Fable iv): see
  followon-instruct/DECODER_PATH_AUDIT.md; suite at 15 decoder tests / 137
  total, all passing at the freezing commit.
- Corrected data is primary for both rungs; as-run randomized data is
  superseded history retained with the defect notice (Fable, 10.1).
- Per-arm/cell resumed counts and full validation summary published (Sol 5):
  `repair_report_{rung}.json`, `validation_report_{rung}.json`.

## Environments (from the frozen manifests; no knobs)

- followon: Qwen/Qwen2.5-7B-Instruct @ a09a35458c702b33eeacc393d103063234e8bc28,
  terminal set {<|im_end|>, <|endoftext|>}, extended extraction,
  max_new_tokens 1024, lookahead 100, bf16 CUDA, transformers 5.14.1.
- rung1: Qwen/Qwen2.5-7B @ d149729398750b98c0af14eb82c78cfe92750796,
  frozen single-EOS terminal, frozen extraction, same decode params.

## Procedure

scripts/repair_resume.py: sweep -> plan -> execute -> validate per rung.
Resume mechanics: prompt recovered as text[:prompt_chars]; per-problem RNG
rebuilt by replaying logged eligible-set draws with draw-by-draw equality
verification; fixed decoder resumed with the chopped text as its prefix
(state-equivalent to the correct code's post-splice state: same realized
string, same canonical re-encoding, same frontier, ended cleared); remaining
token budget = 1024 - (tokens(chopped) - tokens(prompt)). Non-chopped
records copied verbatim with {"repair": {"resumed": false}}.

## Blinding

Embargoed as-run analysis outputs (analysis_followon.json,
decomposition_followon.json) deleted before this freeze per Sol 10.3.
Party rulings were made blind to all outcome numbers. The implementer's
diagnosis necessarily saw partial outcome-adjacent data (logged in
REVIEW_LOG per Fable 10.3); the corrected analysis runs only after
validation passes.
