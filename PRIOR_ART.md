# PRIOR_ART.md — Literature Landscape and Novelty Assessment

Compiled 2026-08-06 from a six-search sweep across the CoT-faithfulness,
steganography/monitorability, trace-intervention, and RL-training-effects
literatures. Claude Code: read this before starting. It tells you what the field
has done, what our design adds, and where the time pressure is.

**Publication intent: we plan to write this up formally after testing completes.**
Engineering choices should anticipate that — keep run configs, seeds, manifest
hashes, raw outputs, and analysis scripts organized as if a Methods section will be
written from them. The pre-registration (SPEC.md + FREEZE_MANIFEST.json + git
history) is itself a headline feature of the eventual paper: the field below is a
pile of contradictory directional findings with no pre-registered adversarial
predictions, and a priced disagreement between two frontier models is the gap we
fill. Nothing in this file modifies SPEC.md; prior art does not change frozen
registrations.

---

## 1. The conceptual framing is already published — by both sides

- **Emmons et al. 2025, "When Chain of Thought is Necessary, Language Models
  Struggle to Evade Monitors" (arXiv:2507.05246, Google DeepMind).** Introduces
  CoT-as-rationalization vs. CoT-as-computation, grounded in the serial-depth
  argument (models must externalize intermediate reasoning when computational
  depth exceeds a single forward pass). This is Fable's two-regime opening claim,
  in print. Also finds: when CoT is load-bearing, monitor evasion degrades
  accuracy — partial evidence for the readable-channel-carries-load view.
- **Levy et al., Dec 2025, "State over Tokens" (arXiv:2512.12777).** Reframes
  reasoning tokens as externalized computational state — the sole persistent
  information carrier across stateless generation cycles — that can drive correct
  reasoning without being a faithful explanation when read as text. This is Sol's
  ontology, in print. Crucially a POSITION paper: explicitly lists "whether
  natural language possesses unique advantages as a computational medium" as an
  open direction. Our experiment is aimed at exactly that open direction.
- **Korbak et al. 2025, "Chain of Thought Monitorability: A New and Fragile
  Opportunity" (arXiv:2507.11473).** Multi-lab position paper: outcome-based RL
  may erode legibility; monitorability is contingent on training practice.
  Motivates our rung 4 axis.

Implication: neither dialogue position was novel. The MEASUREMENT is the
contribution — nobody has isolated channel-1-minus-channel-2 (task state carried
by reader-neutral token distinctions) in ordinarily-trained models, nor measured
its depth interaction.

## 2. Rung-by-rung novelty assessment

### Rung 1 — Neutral-choice randomization: NOVEL, closest call
Nearest work: "Are Reasoning LLMs Robust to Interventions on their
Chain-of-Thought?" (arXiv:2602.07470, Feb 2026). Intervenes mid-trace with
benign/neutral/adversarial edits; finds graceful degradation, several models >97%
accuracy after five consecutive interventions. BUT: interventions are coarse
(segment rewrites, noise injection), there is no logit-eligibility criterion, no
restriction to reader-neutral alternatives, and no depth-interaction observable.
Their robustness findings weakly favor Fable's flat prediction without isolating
the channel. Input-side perturbation work (GSM-Symbolic; lexical/syntactic
sensitivity benchmarks) shows reasoning is sensitive to surface form of the
PROBLEM — distinct from our intervention on the model's OWN generated trace.
Status: our design appears unclaimed. Run first.

### Rung 2 — Correlation-broken resampling: defense literature exists, the
measurement use does not
- Roger & Greenblatt 2023 (arXiv:2310.18512): paraphrase defense bounds learned
  encoding schemes to ~3 bits/KB. Canonical prior art for the sanitizer concept.
- Mathew et al. 2024 ("Hidden in Plain Text"): paraphrasing does not robustly
  mitigate 1-bit payloads; against a LEARNING collusion team, a context-aware
  paraphraser reduced capacity only ~24%.
- "Conceptual Steganography" (arXiv:2605.26537, May 2026): constructs schemes
  robust to paraphrase by encoding in conceptual rather than lexical space;
  encoded CoTs preserve reasoning utility. Empirically vindicates Sol's closing
  correction — the sanitizer prices a NAMED equivalence class, not monitorability
  in general. Cite it wherever the sanitizer's guarantee is described.
CRITICAL GAP: every paper above uses deliberately induced payloads (trained or
prompted collusion). Nobody measures whether ordinarily-trained models
SPONTANEOUSLY carry task state in the neutral channel. That is our question, and
it is open.

### Rung 3 — Probe + intervention on neutral patterns: confound validated,
probe unrun
"Lexical Hints of Accuracy in LLM Reasoning Chains" (arXiv:2508.15842): lexical
uncertainty markers in CoT are the strongest predictors of incorrect answers.
This PROVES the content-conditioned-baseline repair in our design was necessary —
surface features trivially correlate with difficulty. Commitment-timing probe
work ("Reasoning Theater", Boppana et al. 2026; "When Reasoning Traces Become
Performative", arXiv:2605.11746) probes WHEN answers lock in, not whether neutral
surface patterns carry decodable task state beyond the readable trace. Our probe
(with the beyond-content baseline) appears unrun.

### Rung 4 — Training-history axis: HOTTEST, highest scoop risk
- "Monitorability as a Free Gift" (arXiv:2602.03978, Feb 2026): early RLVR can
  IMPROVE monitorability, but the effect is data-dependent, not universal.
- RL-finetuned VLM study (arXiv:2602.12506): faithfulness generally DECREASES
  over RL training, even with augmentation.
- Anthropic-adjacent LessWrong study (Jan 2026): RL pressures (high temperature,
  KL, length budgets) produce illegible/nonsense tokens alongside legible
  reasoning — "not encoded reasoning."
- "Predicting When RL Training Breaks Chain-of-Thought" (Alignment Forum, Apr
  2026): conceptual framework for when optimization degrades monitorability.
- Baker et al. 2025: CoT-pressure during RL induces obfuscated reward hacking.
The field is contradictory in a way our checkpoint design (OLMo 2 / Tülu 3
SFT/DPO/RLVR stages, neutral-penalty measured per stage) could arbitrate. Nobody
has run it. But this rung has the shortest half-life — prioritize after rungs
1–2, and check for new checkpoint-based results before running.

## 3. Evidence leanings entering the experiment (context, not registration)

- Toward Fable (flat depth interaction on base/light-instruct): mid-trace
  intervention robustness (2602.07470); Emmons load-bearing/evasion-cost result;
  "not encoded reasoning" findings under RL pressure without outcome-filtered
  selection on style.
- Toward Sol (neutral channel carries load / sanitizer insufficiency):
  conceptual steganography's paraphrase-robust channels; Mathew et al. 1-bit
  persistence; GSM-Symbolic-style surface sensitivity; steganographic collusion
  emerging from misspecified rewards.
Both leanings come from adjacent designs, not ours. The registrations in SPEC.md
§6 stand unmodified.

## 4. Operational consequences for Claude Code

1. Rungs 1–2 first, fast — cheap, cleanly novel, and what the position papers
   are asking for.
2. Rung 4 is time-sensitive: re-search for staged-checkpoint neutral-penalty
   work immediately before committing GPU time to it.
3. Before EACH rung's main run, do a quick novelty re-check (search the arXiv
   listing for the past ~3 months with the vocabulary above plus: "surface-form
   sensitivity", "lexical robustness of reasoning", "reader-equivalent",
   "token-choice randomization"). If scooped on a rung, the frozen design still
   runs — replication with pre-registration retains value — but flag it to Noah
   before spending.
4. Keep a running BibTeX file (writeup/references.bib) from day one; add every
   paper in this file plus anything new the re-checks surface.

---

## Rung 1 pre-run novelty re-check — 2026-08-08 (per item 3 above)

Two-query sweep during calibration, before main-run GPU spend. New adjacent
work since the freeze sweep, none claiming the rung 1 design:

- arXiv:2605.07307 "Rethinking Dense Sequential Chains" — line-level CoT
  shuffling costs <0.5pp accuracy, word-level retains 62-89%, token-level
  collapses. Destroys ORDERING (protected channel 2 in our design); no
  neutrality restriction, no eligibility criterion, no depth axis.
- arXiv:2605.16874 "Reasoning Can Be Restored by Correcting a Few Decision
  Tokens" — a small set of pivotal tokens dominates outcomes; corrective,
  not neutrality-constrained intervention.
- arXiv:2604.15726 "LLM Reasoning Is Latent, Not the Chain of Thought" —
  position paper adjacent to the latent-vs-serialized carve; no
  channel-1-minus-channel-2 measurement.
- arXiv:2605.29087, arXiv:2606.13603 — trace-answer dissociation and
  commitment-boundary probing; rung 3 adjacent.

VERDICT: rung 1 design still unclaimed; clear to run.
5. Write-up intent means: never discard raw generations; log per-site
   intervention records; keep the analysis notebook reproducible end-to-end from
   FREEZE_MANIFEST.json + seeds.

---

## Addendum 2026-08-15 — Sampling watermarks: a deployed industrial application
## of the assumption we test

On 2026-08-11 Anthropic announced sampling-based text watermarking for Claude
outputs (anthropic.com/news/claude-text-watermark; support.claude.com article
16266773), driven by the EU AI Act's transparency code (effective 2026-08-02).
Mechanism per their own explainer: at generation steps where several next tokens
are "low-stakes" (near-equiprobable, their example: "overcast" vs. "grey"), the
choice is settled not by a fair random draw but by a keyed pseudorandom function
of a secret key plus a few preceding words — leaving a reader-invisible,
key-detectable statistical pattern. Method family in the literature:
Kirchenbauer et al. 2023 (arXiv:2301.10226, logit green-listing), Aaronson's
Gumbel trick, Kuditipudi et al. 2023 (arXiv:2307.15593, distortion-free
schemes), SynthID-Text (Dathathri et al., Nature 2024) — which Anthropic cites
for its no-quality-impact evidence.

Relevance to us — application, not scoop risk:

- The deployment premise is exactly our contested quantity. "The choice doesn't
  matter to the reader" is a channel-2 statement; watermark quality evaluations
  (side-by-side human ratings, SynthID's user studies) certify channel 2 only.
  Whether the realized neutral choice matters to the MODEL's own downstream
  computation when the trace is consumed as CoT — channel 1 minus channel 2 —
  is untested by that literature and is our registered question.
- The operational locus is the same as ours: decode-time re-settling of choices
  among near-equivalent candidates. Our randomized arm (uniform resample within
  Δ = 1.5 nats at reader-neutral rule sites, generation continuing conditioned
  on the result) is a harsher, site-restricted cousin of a sampling watermark
  applied to a reasoning trace.
- Rung 1's rule-05 termination finding is a concrete caution for the genre:
  a "low-stakes" whitespace choice was load-bearing via the termination
  mechanism on the base checkpoint. Equiprobable does not imply inconsequential.
- Even distortion-free schemes (distribution-preserving in aggregate) fix
  particular realizations; whether particular neutral realizations carry task
  state for the same model's continuation is untouched by the distortion-free
  guarantee.

No novelty threat to any rung: nothing in the watermarking literature measures
spontaneous neutral-channel task state or its depth interaction. Framing
material and operational consequences (judge determinism check) are in
writeup/watermarking_context.md. Nothing here modifies frozen registrations.
