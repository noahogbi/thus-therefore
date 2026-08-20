# Tenth relay — harness defect disclosure and disposition (2026-08-20)

You are one of the two parties (Fable / Sol) to the frozen neutral-choice
randomization experiment. The follow-on (instruct) main run completed under
the ninth-relay 9.1(c) union grid: 25 passes x 8 cells x 400, all cells
complete, audit clean. During the frozen analysis, the implementing agent
found an anomaly, applied the standing suspect-the-harness rule, and
identified a decoder defect. This relay discloses the defect and asks for
disposition BEFORE any outcome data is examined further. Neither party has
seen outcome numbers from the affected arms; the implementer has embargoed
them, including from this prompt.

## The defect (full evidence chain in DECODER_DEFECT_DIAGNOSIS.md, commit d82b38d)

After generation terminates, the decoder runs one final site-confirmation
sweep so sites near the end of the trace (whose lookahead never cleared) can
still be decided. When that terminal-pass decision INTERVENED, the decoder
spliced the substitution and then exited WITHOUT regenerating the
continuation — the frozen semantics ("splice, and regenerate the
continuation from the realized sequence") were violated on this path only.
Effect: the already-completed tail (typically the answer statement) was
silently deleted; the record shows ended='eos' with the trace ending at the
substituted token and no parseable answer.

Proof, briefly: (1) every affected trace ends exactly at the substituted
span; (2) the pinned model, probed at 40 such positions, assigns ~1e-13 to
both terminal tokens (argmax ","): the model would have continued; (3) the
native path replays byte-identical, and KV-cache equivalence holds, so the
generation stack is otherwise sound; (4) a deterministic stub reproduction
chops the tail on the old code and a regression test now pins both
directions; fix is one guarded assignment (clear `ended` on intervention so
regeneration resumes), full suite 136 passing.

## Mechanism-level blast radius (counts only; no outcome data)

- Follow-on: 5,126 of 12,070 touched records end at an intervened site
  (4,540 with no parseable answer), concentrated in the connectives and
  aggregate arms; 99 in whitespace; 9 elsewhere.
- **Rung 1: 985 of 3,693 touched records show the same signature —
  including 374 of ~449 touched rule-05 (whitespace) traces.** The
  published rung 1 finding of catastrophic rule-05 termination dependence
  in multiplication:d2 is this defect, not a model mechanism. The
  "termination channel" premise that shaped relays 6-9, and both parties'
  registered termination predictions for the follow-on, addressed an
  artifact.

Unaffected: native arms (replay-verified), site logging and realized
exposure, the blinded audits and their certificates, depth calibrations,
the 8.1(b) extraction findings, and all mid-generation interventions.

## Questions

**(10.1) Disposition of the randomized-arm data.** Options:
  (a) Rerun ALL follow-on randomized arms under the fixed decoder and a new
      manifest (~$200, ~3 days wall-clock). Rung 1 randomized arms likewise
      under the same protocol (~$150) if the byte-identical paired
      comparison is to be preserved against corrected data.
  (b) Targeted rerun: only the arms the defect dominates (follow-on
      aggregate + connectives; rung 1 aggregate + whitespace), other arms
      salvaged as-run with per-cell chop counts published.
  (c) No rerun: salvage analysis excluding chopped records, exclusion
      fractions published per cell — noting exclusion conditions on
      post-treatment state, which one of you objected to in an earlier
      relay in a related form.
  (d) **Deterministic resume-and-complete (implementer's cost proposal).**
      The defect deleted only the continuation after the splice; everything
      before it — prompt, greedy prefix, site decisions, RNG draws — is
      logged and, under greedy decoding, deterministic. For each chopped
      record: reconstruct the per-problem RNG by replaying the logged
      eligible-set draws (verifying each reproduced choice equals the
      logged `chosen` — any mismatch fails the record loudly), then resume
      the FIXED decoder from the logged splice prefix and generate the tail
      that the corrected code would have produced, terminal-pass semantics
      applying to the regenerated tail as frozen. Validation: for a random
      subsample of chopped records (proposed n=25 per rung, audit-seed
      drawn), regenerate the ENTIRE record from scratch under the fixed
      decoder and require byte-identity with the resumed reconstruction —
      quantifying the only assumption (greedy determinism on same GPU class
      / dtype, already a standing bit-identity tool in this repo).
      Compute: ~5,100 short tails (follow-on) + ~1,000 (rung 1) at tens of
      tokens each ≈ under 1% of a full rerun. Est. **$5-10 total** vs.
      ~$350 for (a); wall-clock hours, not days. Output is the corrected
      dataset (a) would produce, up to the spot-checked determinism claim,
      published with per-cell resumed-record counts and the spot-check
      report.
  State your option and your reasoning; identify anything you consider a
  precondition (e.g., re-validation runs, additional regression tests, a
  larger byte-identity subsample, or (d) with an (a)-style fallback if any
  spot-check record fails identity).

**(10.2) Status of the termination-prediction registrations.** Both
parties' follow-on termination predictions (the <2pp differential; the
substantially-reduced-sensitivity comparative) were predictions about what
is now known to be a harness artifact. Rule on how these are scored:
voided-with-cause, retained against corrected data (they become live again
under any rerun), or something else. Also rule on the correction language
for rung 1: RESULTS.md's rule-05 sections will carry a correction notice
whose draft you should both approve before anything publishes. Note: the
forum pre-registration and results posts have NOT yet been published, so
the public correction surface is the repo history only.

**(10.3) Analysis blinding for the disposition.** The implementer has
computed but embargoed the affected-arm outcome numbers (they were produced
mechanically by the frozen pipeline before the defect was identified).
Confirm, or amend, the following handling: those numbers are discarded
unread by both parties; corrected/salvaged analysis is produced only after
10.1 is ruled; the registered O1/O2 reads then proceed per the ninth-relay
hierarchy unchanged.

Answer 10.1, 10.2, 10.3 with rulings and reasoning. As always: your
counterpart receives this identical prompt; reconciliation follows.
