# Decoder terminal-pass defect — diagnosis (2026-08-20)

Found during the follow-on O1/O2 analysis, before any results were reported
to the parties. Disclosure goes to both parties in the tenth relay; no
outcome-bearing number from the affected arms should be cited until they
rule on disposition.

## The defect

`InterventionDecoder.generate` runs one final site-confirmation sweep after
generation terminates (`terminal=True`), so sites whose lookahead never
cleared mid-generation can still be decided. When that terminal-pass
decision INTERVENED, `_decide_site` truncated the realized text at the
splice point (`realized[:site.start] + chosen`) — and the loop then hit
`if ended is not None: break` without regenerating, because `ended` was
never cleared. Result: the completed tail (typically ", the product is …
ANSWER: …") was silently deleted; the record shows `ended='eos'` with the
trace ending exactly at the substituted token and no parseable answer.

SPEC semantics (also stated verbatim in tests/test_decoder.py's docstring):
"uniform sample among eligible candidates, splice, and regenerate the
continuation from the realized sequence." The code violated this on the
terminal pass only. Mid-generation interventions were correct.

## Evidence chain

1. **Anomaly:** follow-on aggregate/connectives O1 huge (multiplication:d2
   0.59) but composed ~entirely of no-parseable-answer on touched traces;
   all such traces end exactly at the substituted connective.
2. **Model probe (GPU):** at the exact chopped positions, the instruct
   model's next-token distribution puts ~1e-13 on both terminal tokens;
   argmax is "," in 40/40 probed cases (runs/followon/probe_result.json).
   The model would have continued; the harness stopped it.
3. **Native-path validation:** cache-free greedy replay of native traces is
   byte-identical after the prompt prefix; KV-cache equivalence also holds
   on the truncate-swap-reencode pattern. Generation stack is sound.
4. **Deterministic repro:** stubbed CPU reproduction of the decode loop
   chops the tail on a terminal-pass intervention; regression test
   TestTerminalPassRegeneration failed on the old code, passes on the fix.

## Blast radius (mechanical count: last intervened site == end of text)

Follow-on (instruct): 5,126 of 12,070 touched records chopped (4,540 with
no parseable answer) — concentrated in connectives (~2,500 across its three
seeds) and the aggregate arm (~2,519), plus 99 whitespace, 8 other.
**Rung 1 (base): 985 of 3,693 touched records chopped (983 no-answer) —
including 374 of ~449 touched whitespace traces.** Rung 1's published
"catastrophic rule-05 termination dependence in multiplication:d2"
(RESULTS.md) is this defect, not a model mechanism. The "termination
channel" narrative built across relays 6-9, and both parties' termination
predictions for the follow-on, addressed an artifact.

## What survives untouched

- Native arms (both rungs): no interventions, bit-identical replay verified.
- Density/exposure numbers (site logging happens before the defect).
- The blinded audit and its 100% neutrality certificates (excerpt pairs are
  built from site records, not from the continuation).
- Depth calibrations, the 8.1(b) amendment's extraction findings.
- Mid-generation interventions (6,944 follow-on / 2,708 rung 1 touched
  records not chopped) — but per-record salvage vs. rerun is a party
  decision, not an implementer's.

## Fix

harness/decoder.py: clear `ended` when a decided site actually intervened,
so regeneration resumes from the splice (one guarded assignment; terminal
re-checks then apply to the regenerated tail as frozen semantics require).
Regression tests added (tests/test_decoder.py::TestTerminalPassRegeneration,
both directions). Full suite: 136 passed.

## Disposition options (for the parties; implementer recommends none)

(a) Rerun all randomized arms of the follow-on under the fixed decoder and
    a new manifest (~$200, ~3 days); rung 1 randomized arms likewise if the
    paired comparison is to be preserved (~$150).
(b) Targeted rerun of chopped-dominant arms only (aggregate + connectives
    on instruct; aggregate + whitespace on base), others salvaged with the
    chop-count published per cell.
(c) Analysis-only salvage (exclude chopped records, report exclusion
    fractions) — noting this conditions on post-treatment state.
Either way, RESULTS.md's rule-05 sections need a correction notice, and the
watermarking framing docs must drop the "termination channel" caution in
its current form (writeup/watermarking_context.md flagged).
