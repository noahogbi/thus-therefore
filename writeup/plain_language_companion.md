# Plain-language companion to the results post

Written for Noah pre-publication; kept in the repo because readers may find
it useful too. Nothing here is a claim the post doesn't make — it's the
same content in plain words, plus answers to the questions the comment
section is most likely to ask.

## 1. The question, in plain words

When a model writes out its reasoning, it makes thousands of tiny wording
choices that don't matter to any reader: "thus" vs "therefore," `x=17` vs
`x = 17`, "don't" vs "do not." The question: are those choices *actually*
meaningless, or is the model using them as scratch space — encoding
something it needs later, invisible to anyone reading? If the latter, then
tools that rewrite model reasoning (paraphrase-based safety monitors,
watermarks, trace compression) could silently break the model's thinking
while the text still looks fine. Fable predicted the choices are
meaningless on models like these; Sol predicted they carry load that grows
with how hard the problem is.

## 2. What we actually did, concretely

The model solves a math or graph problem, writing its reasoning step by
step. Our decoder watches for moments where (a) a frozen rule says two
wordings are reader-equivalent, AND (b) the model itself rates both as
near-equally likely (within 1.5 nats — roughly, the less-preferred option
is at least ~22% as likely as the preferred one). At those moments only,
we flip a fair coin among the near-equal options, splice in the winner,
and let the model keep writing from there. Everything else is the model's
untouched first choice. Example: the model has written "…5476 + 74 =
5550.\n\nTherefore" — it also rated "Thus" nearly as likely — the coin
picks "Thus" — generation continues. If wording is scratch space, forcing
the coin-flip should hurt accuracy, and hurt more on deeper problems.
A separate frozen judge model then audited 500 randomly sampled
substitutions per run, blind, against five criteria (same claims, same
logical structure, same hedging, etc.): 1000/1000 passed.

## 3. What each headline number physically means

- **Aggregate O1 = +0.008 (instruct):** with all seven rules randomizing
  at once, accuracy dropped 0.8 points out of 100 — e.g. from 64.5% to
  63.7% in a typical cell. The 95% CI [−0.009, +0.024] means the data are
  statistically consistent with anything from "no effect at all" to "a
  ~2-point effect."
- **Primary slope +0.007 per depth step:** going from depth-4 problems to
  depth-8 problems, the penalty grew by about 0.7 points per step — so
  roughly 2.8 points more penalty at d8 than d4 *if you take the point
  estimate at face value*, which the CI ([−0.011, +0.024], includes zero)
  says you shouldn't. Sol registered only the *sign* of this number, and
  the sign came out positive in all three seeds — that's why Sol's
  prediction "stands narrowly" while everyone agrees it isn't resolved.
- **"~97.5% of candidate sites are closed":** at 97.5% of the places where
  our rules *could* apply, the model wasn't actually torn between two
  wordings — it strongly preferred one. The channel barely exists as a
  set of genuine choices.
- **"1.72 bits per trace":** if you tried to use the model's genuine
  coin-flip moments to smuggle information, an entire reasoning trace
  gives you about 1–2 bits — one or two yes/no answers — on instruct, and
  usually *zero* on base. (log2 of the number of near-equal options,
  summed over eligible sites.)

## 4. The two failures, and why they should increase your trust

**Failure 1 — the decoder bug.** When a substitution site was decided
after the model had already finished its answer, the decoder deleted the
finished answer and never regenerated it. This produced spectacular fake
results (a 59-point penalty!) that flattered one side's hypothesis. It was
caught because the repo's standing rule is "if a result looks wrong,
suspect the harness first" — the model was probed at the exact cut points
and turned out to want to keep writing (probability of stopping: ~1 in
10^13). Everything was re-derived, the affected pre-bug "findings" were
retracted by name, and both models' predictions about the fake phenomenon
were voided rather than scored.

**Failure 2 — the determinism gate.** To validate the repair we demanded
byte-identical regeneration — and discovered that GPU floating-point math
makes greedy decoding not exactly repeatable *even on the same machine*:
at near-ties, different runs occasionally pick different tokens. So the
gate was replaced (by both parties' ruling) with a certification that
every repaired token was the model's argmax or within measured float noise
of it: 6.48M tokens checked, 99.8%+ exact, 2 records excluded.

The reason to trust the numbers is not that nothing went wrong — it's that
the things that went wrong were found by the project's own rules, disclosed
completely, and corrected under adversarial sign-off before anyone treated
the outputs as results.

## 5. Anticipated questions, with answers

**"Only 7B, only Qwen, only synthetic tasks — why should I care?"**
Correct, and the post says so. This is one model family at one scale under
one rule set. The contributions that generalize are the instrument (frozen,
reusable, now battle-tested), the protocol, and the capacity measurement
method. The registered predictions were deliberately written across a
training-regime axis, and the regime where covert encoding is most
expected (outcome-filtered RL) is explicitly untested.

**"Why greedy decoding? Nobody uses greedy in production."**
Greedy makes the estimand clean: there is exactly one native trajectory to
compare against, and the intervention is the only randomness. Sampling
would add noise that swamps sub-point effects at this budget. Cost: the
results are about greedy trajectories; extending to sampled decoding is
future work.

**"The slope is positive in all three seeds — isn't that basically
significant?"** The three seeds re-randomize which alternative gets
spliced, over the *same* 400 problems per cell. They're robustness checks
against coin-flip luck, not independent replications. The frozen CI on the
slope includes zero. Sol itself insists on "directionally supported, not
statistically resolved."

**"You 'repaired' data — isn't that fabrication?"** The bug deleted the
ends of 6,049 traces. The repair kept everything the model actually wrote
and let the *fixed* decoder continue from the exact cut point — then
verified, token by token, that the continuation was the model's own
preferred next token (or within measured float noise). A full rerun was
priced ($350) and rejected by both parties because GPU nondeterminism
means a rerun can't reproduce the originals either — it just draws new
samples. Two records that couldn't be certified were excluded and
published as exclusions. Every step is in REPAIR_PLAN.md and the
certification reports.

**"Did Anthropic and OpenAI actually run this / endorse this?"** No.
The 'parties' are commercial models accessed as products by one
independent person; no lab was involved, consulted, or endorsed anything.
"Fable (Anthropic)" identifies which company *makes* the model, nothing
more. The post frames their role procedurally for exactly this reason.

**"Isn't the model-debate thing just roleplay theater?"** The device is
procedural, not mystical: two models produced frozen, hash-timestamped
predictions and scoring rules *before* data existed, and the git history
proves the ordering. Whether you think models "really" disagree is
irrelevant to what the protocol delivers: predictions that could not be
revised after the results were known — including the parts where each
model's prediction failed.

**"Maybe Δ = 1.5 nats is too strict — the channel looks empty because you
defined it narrowly."** Plausible! The threshold was frozen before data,
so it isn't post-hoc, but the capacity claim is explicitly conditional:
*this rule set, this threshold, these checkpoints*. A looser threshold or
richer equivalence classes (sentence order, phrasing) would define a
bigger channel — and that's a different experiment (and part of why the
headline says "under this rule set").

**"Couldn't the model hide state in the 97.5% of sites where it strongly
prefers one form?"** Then it wouldn't be hiding state in a *choice* — it
would have to systematically write off its own preferred distribution,
which is a learned-encoding story. That's precisely the outcome-filtered
training question (unrun), not something this design can rule in or out.

**"What's the weird d6/d8 thing?"** The all-rules-together arm shows a
~3-point penalty at mid-depths that no single-rule arm shows — even the
rule carrying 74% of its interventions. Unregistered, unpowered (CIs
include zero), reported descriptively, and both models declined to claim
it. Honest answer: nobody knows; it's first in line for the next
pre-registration.

**"Watermarks don't touch chain-of-thought, so why does this matter?"**
Three answers: (1) the industry keeps watermarks out of reasoning *on an
untested assumption* and pays a capacity tax for it (answers are short;
reasoning has the tokens) — this is the first direct measurement under
that assumption's strongest nearby form; (2) the boundary is unstable —
capacity pressure pushes toward marking longer text; (3) in agent loops,
yesterday's watermarked *output* is today's reasoning *input* — "downstream
of CoT" is a one-turn property. Also our capacity numbers say reasoning
text has very little watermarkable slack in the reader-neutral channel to
begin with.

**"Where's the data?"** Everything: raw datasets for both runs
(tarballs + SHA-256), the corrected datasets with per-record provenance,
every analysis script, all 12 relay transcripts, both defect diagnoses,
and the certification reports — all in the repo, all in the git history.

**"What result would have changed the conclusion?"** A penalty that
cleared its CI in the powered cells and grew with depth would have scored
Sol's registration as fully standing and Fable's as fallen — Fable
pre-committed to exactly that ("I lose cleanly and will say so"). It
didn't happen. Conversely, Fable's exposure prediction *did* fail and is
scored as fallen, in its own words.

## 6. The one-paragraph version, for saying out loud

We took a small open model, found the moments where it was genuinely torn
between two wordings that mean the same thing to any reader, flipped fair
coins there, and measured whether its answers got worse. Barely — under a
point on average, with confidence intervals straddling zero — though the
hurt trended very slightly larger on deeper problems, matching the sign
one model predicted but nowhere near statistical resolution. The bigger
surprise: those genuinely-torn moments are incredibly rare. The model
almost always knows exactly which wording it wants, so the "hidden
channel" people worry about is, at least for this family of wording
choices, mostly not there to use. Two frontier models bet on the outcome
in advance, in public, and each lost something; the harness broke twice
and the process caught it both times. The dangerous case — models trained
with RL on outcomes — is the next experiment.
