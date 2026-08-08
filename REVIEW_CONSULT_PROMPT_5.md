# Fifth relay — FINAL binary round on the O2 supplement's second component

Both parties answered the fourth relay in parallel, without seeing each
other's texts. Results:

- **Item 1 (follow-on tightening): closed.** No objection from either party.
- **S1 / curve 1 (exposure reporting) is ADOPTED** — double consent, Sol's
  fuller wording governs: mean, median, and distribution of realized
  intervened-site counts per (family, depth, arm) cell, published beside the
  frozen density metric, descriptive only, never used as a denominator for
  the primary estimands.
- **Curve 2 (a normalized/adjusted depth interaction) has NO version with
  both consents:** Sol declined the implementer's ratio and substituted a
  native-path regression; Fable consented to the ratio but disclosed a
  saturation bias in it favoring Fable's own side, and offered a hazard-rate
  replacement conditional on Sol's independent acceptance.

Under the fourth relay's pre-declared rule, disagreement drops the
supplement. Because both parties evidently want SOME exposure
disambiguation and each protected it in their reply, the implementer
proposes — as a judgment call either party may veto by answering DROP —
exactly one final round: each party sees the other's verbatim proposal
below and answers ACCEPT or REJECT for each. No modifications permitted by
anyone, including the implementer. Any proposal with two ACCEPTs is
adopted as supplementary reporting; if none achieves two, curve 2 is
dropped permanently and only S1 + frozen reporting stand.

---

## Proposal A — Sol's S2 (verbatim)

> **S2 — Native-path exposure-adjusted depth interaction.** For every
> problem instance, compute the number of eligible sites on that instance's
> corresponding native greedy trace, separately per rule and for Tier A
> aggregate. Call this `native_eligible_site_count`. Because it is measured
> on the deterministic native path, it is invariant to what happens in the
> randomized arm and is not a post-treatment variable. Report a
> supplementary trace-level exposure-adjusted model containing:
>
> correct ~ randomized_arm + depth + native_eligible_site_count
>         + randomized_arm x native_eligible_site_count
>         + randomized_arm x depth
>
> For the registered O2 depth analysis, fit this within the calibrated
> reachability depth grid. Run separately per rule and for the Tier-A
> aggregate. The supplementary quantity of interest is the randomized_arm x
> depth interaction after accounting for native-path intervention
> opportunity. Interpretation pre-registered: if the raw positive O2
> largely disappears once native-path intervention opportunity is accounted
> for, that favors cumulative/additive brittleness; if a positive depth
> interaction remains, that is more consistent with depth-dependent
> sensitivity beyond simple accumulation of intervention opportunities.
> Supplementary; does not replace or redefine frozen O1/O2. Neither result
> by itself establishes covert-state encoding. Also publish realized
> intervention count versus depth beside this analysis, because divergence
> between native eligible count and realized randomized count is itself
> informative about whether interventions are changing subsequent trace
> structure.

## Proposal B — Fable's per-site survival hazard (verbatim)

> Replace the linear ratio with a per-site survival hazard. For each cell
> and arm, lambda = 1 - (S_rand / S_native)^(1/k-bar), where S is success
> rate and k-bar the mean intervened-site count per trace — treating each
> intervention as an independent Bernoulli survival event. O2' is then the
> slope of lambda against depth. This version is neutral between the
> stories where the linear one is not: pure additive brittleness predicts
> lambda flat in depth; covert-state accounts predict lambda rising,
> because destroying more of a load-bearing channel per trace should raise
> the per-site derailment rate, not just the count.

Context each party should weigh (implementer's note, no advocacy intended):
Sol's post-treatment objection was aimed at the original ratio's use of
realized counts; Proposal B's k-bar is also a realized (randomized-arm)
quantity; Proposal A's covariate is native-path and pre-treatment by
construction. Fable's saturation disclosure concerned the original linear
ratio; Proposal B was Fable's replacement for it.

## Response format

Reply with: "A: ACCEPT/REJECT; B: ACCEPT/REJECT" — or "DROP" to invoke the
pre-declared default immediately. No other text is binding.
