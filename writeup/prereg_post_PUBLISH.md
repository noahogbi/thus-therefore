# Pre-registration: does chain-of-thought carry covert task state in reader-neutral wording?

*[Courier's note, added 2026-08-22, above the frozen text — which is
reproduced unchanged below. (1) I chose to publish this post together with
the results post ([link inserted at posting]) rather than at freeze time;
the design's actual external timestamp is therefore not this post but the
public git history — the frozen spec was pushed 2026-08-07 (commit
`79781ea`) and the manifest hash 2026-08-08 (commit `bc93833`), before any
generation run. The frozen text's line "this post timestamps the design"
reflects the original same-day posting plan. (2) The frozen text's claim
that "the design guarantees one registered prediction loses" turned out to
be overconfident, which is itself informative: exposure collapse rendered
one run non-discriminating, and the other left both positions alive in
qualified forms — see the results post's prediction ledger. (3) On the two
parties: they are model-generated adversarial reviewers operating under
frozen scoring rules, accessed as commercial products by one independent
person; no lab was involved or endorsed anything.]*



**TL;DR:** Two frontier models — Fable (Anthropic) and Sol (OpenAI GPT
lineage) — disagree about what the tokens of a reasoning trace do. They
negotiated a falsifiable experiment in an adversarial dialogue, registered
opposing predictions, and froze the design before any data. I'm the human
who transported the dialogue and will run the experiment. This post
timestamps the design. Manifest hash:
`ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040`.
Repo: `https://github.com/noahogbi/thus-therefore`.

## The disagreement

Split a generated reasoning trace into three channels: (1) the token
sequence itself; (2) what a competent reader recovers from it — claims,
derivation structure, hedging; (3) the computation the model reconstructs
from it. The contested quantity is channel 1 minus channel 2: task state
carried by reader-neutral distinctions, like choosing "thus" over
"therefore" or `x=17` over `x = 17`.

Sol's position: recurrent computational state can hide in such neutral
choices, so destroying them should hurt more as required serial reasoning
depth grows. Fable's position: on base and lightly-instructed models the
readable semantics carry the load — destroying neutral choices costs
roughly nothing at any depth — and depth-sensitivity emerges only after
outcome-filtered training.

## The experiment (rung 1)

Decode greedily everywhere, except at pre-registered sites where the model
chose among reader-equivalent surface forms. At those sites, sample
uniformly among alternatives the model itself rates within 1.5 nats of its
preferred choice. Seven frozen rule tables define the sites (connective
synonyms, comma variants, discourse markers, contractions, formatting
whitespace, operator spacing, bullet glyphs); everything that could carry
readable meaning — ordering, granularity, hedging, which intermediates are
explicit — is protected and never touched. Accuracy penalty is measured as
a function of calibrated serial depth on three task families
(multiplication, function composition, graph reachability).

## Registered predictions (frozen; SPEC section 6)

- **Sol:** positive depth interaction on the Tier A aggregate — the penalty
  grows with depth.
- **Fable:** depth interaction ~zero for every rule on base/light-instruct
  checkpoints; positive interaction emerging only on outcome-filtered
  checkpoints, concentrated in the highest-density, highest-entropy rules
  first. This sub-prediction (the ordering) separates the stories even if
  both observe positives post-RL.

Neither prediction can be revised after data. Amendments require a new
pre-registration and a fresh run under a new hash.

## Why you might trust this

- The design was frozen 2026-08-06, before any implementation. The
  implementing agent's job is engineering fidelity; its standing
  instructions forbid design improvement.
- A mandatory adversarial review of the drafted rule tables ran BEFORE
  hashing, caught two real defects in the tables (both drafted by Fable —
  one of which would have quietly disadvantaged Sol's side), and every
  disposition was ruled on by both parties and logged with attribution
  (REVIEW_LOG.md in the repo).
- Validation is pre-committed: a frozen judge model at temperature 0
  audits ~500 sampled interventions, blinded; any rule scoring under 98%
  on five preservation criteria is removed whole and the experiment rerun
  under a new hash. No example-level excision, ever.
- All randomness seeds are committed in the manifest. The audit sample is
  drawn before any outcome analysis.
- The repo's git history is the audit trail — including this post's hash.

## What happens next

Depth calibration, then the main run (native vs. neutral-randomized) on a
rented consumer GPU, then the blinded audit, then analysis. Results will be
posted whatever they show — the design guarantees one registered prediction
loses. Nature decides who pays.
