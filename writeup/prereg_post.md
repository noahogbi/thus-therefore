# Pre-registration: does chain-of-thought carry covert task state in reader-neutral wording?

*[Final text â€” hash filled at freeze, 2026-08-08. Voice/edits are Noah's
call; the design content must keep matching the frozen spec.]*

**TL;DR:** Two frontier models â€” Fable (Anthropic) and Sol (OpenAI GPT
lineage) â€” disagree about what the tokens of a reasoning trace do. They
negotiated a falsifiable experiment in an adversarial dialogue, registered
opposing predictions, and froze the design before any data. I'm the human
who transported the dialogue and will run the experiment. This post
timestamps the design. Manifest hash:
`ebb6bca07b1773f1161e593f0fd393c10cdb866f3f121bfa4351c8ff72177040`.
Repo: `https://github.com/noahogbi/thus-therefore`.

## The disagreement

Split a generated reasoning trace into three channels: (1) the token
sequence itself; (2) what a competent reader recovers from it â€” claims,
derivation structure, hedging; (3) the computation the model reconstructs
from it. The contested quantity is channel 1 minus channel 2: task state
carried by reader-neutral distinctions, like choosing "thus" over
"therefore" or `x=17` over `x = 17`.

Sol's position: recurrent computational state can hide in such neutral
choices, so destroying them should hurt more as required serial reasoning
depth grows. Fable's position: on base and lightly-instructed models the
readable semantics carry the load â€” destroying neutral choices costs
roughly nothing at any depth â€” and depth-sensitivity emerges only after
outcome-filtered training.

## The experiment (rung 1)

Decode greedily everywhere, except at pre-registered sites where the model
chose among reader-equivalent surface forms. At those sites, sample
uniformly among alternatives the model itself rates within 1.5 nats of its
preferred choice. Seven frozen rule tables define the sites (connective
synonyms, comma variants, discourse markers, contractions, formatting
whitespace, operator spacing, bullet glyphs); everything that could carry
readable meaning â€” ordering, granularity, hedging, which intermediates are
explicit â€” is protected and never touched. Accuracy penalty is measured as
a function of calibrated serial depth on three task families
(multiplication, function composition, graph reachability).

## Registered predictions (frozen; SPEC section 6)

- **Sol:** positive depth interaction on the Tier A aggregate â€” the penalty
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
  hashing, caught two real defects in the tables (both drafted by Fable â€”
  one of which would have quietly disadvantaged Sol's side), and every
  disposition was ruled on by both parties and logged with attribution
  (REVIEW_LOG.md in the repo).
- Validation is pre-committed: a frozen judge model at temperature 0
  audits ~500 sampled interventions, blinded; any rule scoring under 98%
  on five preservation criteria is removed whole and the experiment rerun
  under a new hash. No example-level excision, ever.
- All randomness seeds are committed in the manifest. The audit sample is
  drawn before any outcome analysis.
- The repo's git history is the audit trail â€” including this post's hash.

## What happens next

Depth calibration, then the main run (native vs. neutral-randomized) on a
rented consumer GPU, then the blinded audit, then analysis. Results will be
posted whatever they show â€” the design guarantees one registered prediction
loses. Nature decides who pays.
