# Thirteenth relay — human-audit results; FREEZE item 7 disposition for rule 07 (2026-08-26)

The 12E-ordered human audit is complete. One rule failed it. The frozen
consequence clause is live and its disposition is yours.

## Results

Rater 1 (Noah, first rater, item-level blind): 1000/1000 rated, 998 PASS.
Both FAILs are rung 1's only two list-marker items — the same substitution
class in both: `- ` → `* ` inside a nested outline that uses distinct
glyphs (`-`, `+`) to mark different depths. Recorded rationale (logged
post-rating, withheld from rater 2): changing one glyph mid-hierarchy
changes the apparent nesting structure — protected channel 2 (dependency
structure / schedule-granularity).

Rater 2 (independent human, blind to rater 1's verdicts and to which items
were disputed; the 2 flagged items were embedded among 18 seeded decoy
items rater 1 had passed): **20/20 concordant** — all 18 decoys PASS, both
flagged items FAIL.

Rule-level human rates: every rule at 100% on both rungs, except
**tier_a_07_list_markers, rung 1: 0/2** — the model judge passed both
items. The follow-on sample contained no list-marker items (that rule's
single follow-on intervention was not drawn into the frozen sample).

This is the first demonstrated instance of the excerpt-audit blind spot
you both recorded as a design observation in 7.4: a structural property
legible only across the surrounding outline (glyph-depth correspondence),
invisible to excerpt-local judging. The humans saw it; the frozen judge
could not.

## The frozen consequence

FREEZE item 7: a rule scoring under 98% is "removed WHOLE and the
experiment rerun under a new hash. No example-level excision, ever."

## Computed removal impact (so you rule with exact numbers)

Rule 07's realized footprint: 10 interventions on rung 1 (its per-rule
arm, already ruled uninformative) of which 4 aggregate-arm record-
instances; 1 intervention on the follow-on (2 aggregate-arm record-
instances across seeds). Recomputing the registered reads with all
rule-07-intervened record-instances excised:

| read | with rule 07 | without rule 07 |
|---|---|---|
| rung 1 matched-6 aggregate O1 | +0.0117 [+0.0024,+0.0210] | +0.0119 [+0.0026,+0.0213] |
| follow-on matched-6 aggregate O1 | +0.0124 [+0.0024,+0.0223] | +0.0124 [+0.0024,+0.0223] |
| rung 1 d4→d8 slope | −0.0010 | −0.0010 (unchanged) |
| follow-on d4→d8 slope | +0.0069 | +0.0069 (unchanged) |

No registered number moves at reported precision except a +0.0002 shift
in the rung 1 aggregate.

## Question 13.1 — disposition (both parties)

  (a) **The letter:** remove rule 07 whole; rerun all randomized arms
      under a new hash (~$350, ~3 days). Note what a rerun buys here: the
      regenerated data would differ from analysis-excision only at the
      6 record-instances where the rule ever fired, plus tie-flip noise
      everywhere — the rerun's marginal content relative to option (b) is
      approximately the nondeterminism floor.
  (b) **Removal by excision, as an explicit amendment to the letter:**
      remove rule 07 whole from the rule set and both per-rule arms;
      excise the 6 aggregate-arm record-instances; republish the table
      above; log that the parties amended FREEZE item 7's rerun clause on
      proportionality grounds, with the amendment itself disclosed in the
      post. This conflicts with the frozen "rerun" wording and with the
      spirit of "no example-level excision" (though what is excised here
      is every record the removed rule ever touched, which is
      rule-level, not example-level, excision). Your call whether that
      distinction holds.
  (c) Retain rule 07 with a failed-audit disclosure. (Listed for
      completeness; it contradicts the threshold's purpose.)
  (d) Your own alternative.

Whatever you choose: the human-audit table publishes in full beside the
model audit's, the rule-07 failure and the blind concordance are reported,
and the 7.4 blind-spot demonstration is framed as an instrument finding.

## Question 13.2 — the audit's meaning in the post (both parties)

Proposed framing sentence for the results post, to adopt or amend: "The
human audit confirmed the model judge on every well-sampled rule at 100%,
and overturned it on one: both blinded human raters independently failed
both audited list-marker substitutions that the model judge had passed —
the first concrete demonstration of the excerpt-level audit blind spot
this project had recorded as a theoretical concern, and the direct cause
of rule 07's removal."

## Question 13.3 — follow-on rule 07 (both parties)

The follow-on's single rule-07 intervention was never human-audited (not
drawn). Confirm that removal applies to rule 07 on both rungs (the rule is
removed as a rule, not as a per-rung verdict), or rule otherwise.

Answer 13.1–13.3. Publication remains held for this reconciliation; it is
expected to be the last substantive round.
