# Seventh relay: rung 1 results, and a mechanism the frozen audit cannot see

You are one of the two registered parties (Fable / Sol). Both ruled **6b**
in the sixth relay; the analysis was computed exactly as ruled — O1/O2 per
rule and aggregate, three intervention seeds, S1 exposure reporting, and
the Proposal A exposure-adjusted model — with no cell, estimand, or
analysis altered on account of measured exposure. Results below. One
finding requires rulings before anything is written up as a claim.

## 1. Registered results

O1, mean accuracy penalty pooled across the three intervention seeds
(native minus randomized, averaged over the six ruled cells):

| arm | interventions | O1 |
|---|---|---|
| Tier A aggregate | 1,946 | **+0.055** |
| tier_a_05_whitespace | 471 | **+0.043** |
| tier_a_01_connectives | 245 | +0.007 |
| tier_a_06_operator_spacing | 483 | +0.002 |
| tier_a_04_contractions | 158 | +0.000 |
| tier_a_02_punctuation | 547 | −0.005 |
| tier_a_07_list_markers | 10 | +0.003 (uninformative, per your sixth-relay rulings) |
| tier_a_03_discourse_markers | 0 | structurally unavailable, not a null |

O2, reachability family: aggregate slope −0.009; restricted d4→d8 slope
−0.0004. Per-rule slopes all within ±0.005. Per your pre-declared
non-discrimination statements, these are published as underpowered
secondaries and claimed by neither party. Proposal A arm×depth
coefficients are reported in the committed analysis JSON.

Seed consistency is tight (aggregate O1 by seed: +0.055, +0.051, +0.058).

## 2. The aggregate O1 is one cell, and its mechanism is termination

The +0.055 aggregate is not distributed. It is almost entirely rule-05
whitespace interventions in **multiplication:d2**: penalty +0.211,
z ≈ 7.4, consistent across all three seeds. Every other rule × cell
combination is within noise.

Decomposing that cell by whether a trace actually received an
intervention (seed 271828; the other two seeds match within 3%):

| group | n | correct | wrong number | **no parseable ANSWER** | mean tokens |
|---|---|---|---|---|---|
| native | 400 | 229 | 161 | 10 (2.5%) | 128 |
| randomized, untouched | 274 | 141 | 123 | 10 (3.6%) | 142 |
| randomized, **touched** | 126 | 1 | 3 | **122 (97%)** | **88** |

All 126 touched traces ended on EOS, not truncation. The penalty is
therefore not degraded arithmetic; the model **stopped generating**.
Representative case, same problem, native versus randomized:

```
NATIVE      ... Step 2: Calculate the product of 74 and 75.\n\n74 * 75 = 5550\n\nAnswer: 5550
RANDOMIZED  ... Step 2: Calculate the product of 74 and 75.\n          [EOS]
```

The rule-05 swap of `\n\n` for `\n` at an existing paragraph boundary
appears to remove a continuation cue: in this base model a blank line after
a step reads as "another block follows," a single newline as
end-of-document. The effect concentrates where traces are short and highly
structured (multiplication:d2 native traces average 128 generated tokens).

**The frozen audit passed rule 05 at 100% on 130 items, and was correct to
do so.** SPEC section 8's five criteria judge whether the swap preserves
propositions, dependency structure, hedging, explicit-intermediate
selection, and schedule/granularity *within the excerpt*. It does. No
criterion asks whether the swap changes what the model generates *next*.
This is a blind spot in the validation protocol, discoverable only by
running the experiment.

## 3. The interpretive question, stated without advocacy

A reader recovers nothing semantic from `\n\n` versus `\n`. By the frozen
definition in SPEC section 1, this is therefore the reader-neutral channel
carrying something the model demonstrably acts on. What it carries is
document-structure state — continue versus stop — rather than intermediate
task state of the kind the depth hypothesis concerns. The implementer takes
no position on whether that counts.

## 4. Rulings requested

**(7.1) Reporting of the rule-05 and aggregate O1.** Choose one:
- (a) Report the raw penalties as computed, unqualified.
- (b) Report the raw penalties as computed, with the termination
  decomposition published alongside as a required companion.
- (c) Report the raw penalties, and additionally report the aggregate
  excluding rule 05, clearly labeled as a decomposition rather than a
  substitution.
- (d) Other (specify).

**(7.2) Answer-extraction failures in O1.** The frozen O1 counts a trace
with no parseable ANSWER line as incorrect. Should the writeup
additionally report, as a supplementary decomposition, accuracy split into
"wrong number" versus "no parseable answer" per arm and cell? (consent /
decline / modify). This changes no frozen estimand.

**(7.3) Framing.** Is the termination dependence (a) an instance of the
contested channel-1-minus-channel-2 quantity, (b) a distinct phenomenon
requiring its own name and separate reporting, or (c) an artifact of the
harness/task format to be reported as a limitation? A one-line
characterization from each party will be quoted in the writeup.

**(7.4) Audit blind spot.** Should the writeup record explicitly that the
frozen five-criterion audit certifies excerpt-level neutrality but cannot
detect downstream continuation effects, and that a future pre-registration
should consider a sixth criterion or a continuation check? (consent /
decline / modify wording).

**(7.5) Non-binding.** Does this change anything about the pre-registered
light-instruct follow-on — for example, whether instruction tuning (which
trains models to complete responses) is expected to remove or preserve the
termination sensitivity, and whether that is worth stating as a prediction
now, before that run?

## Response format

Reply with 7.1 (a/b/c/d), 7.2, 7.3, 7.4, and optionally 7.5. Fable's
standing conservative tiebreak governs reconciliation. No frozen estimand
is being changed by any option; all rulings concern reporting and framing.
Nothing will be written up as a claim before both replies are reconciled.
