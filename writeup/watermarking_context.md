# Watermarking context and framing plan (2026-08-15, non-frozen)

Compiled after Anthropic's watermarking announcement (2026-08-11), which
postdates the design freeze (2026-08-06), the manifest hash, and both parties'
registered predictions. The follow-on's ninth-relay grid ruling was
contemporaneous with the announcement and involved no design changes. Nothing
in this file modifies frozen registrations; it is raw material for the results
post, the paper's Intro/Related Work/Discussion, and operational checks.

## 1. What Anthropic announced (the facts)

- **What:** Invisible statistical watermarks in Claude-generated text, plus
  C2PA signed provenance metadata in generated files (.png/.jpg/.svg).
  Announced 2026-08-11; policy effective for models launched on or after
  2026-08-02; older models "retrofitted over the coming months." No opt-out.
  Worldwide, all surfaces: Claude Platform (API), claude.ai, Claude Code,
  Cowork, Claude Tag; cloud partners (AWS, GCP, Microsoft Foundry) with
  platform caveats.
- **Why:** EU AI Act Article 50 / transparency code (effective 2026-08-02);
  200+ signatories including OpenAI, Google, Meta, Microsoft.
- **Mechanism (their explainer):** At generation steps where several next
  tokens are near-equiprobable ("The weather today was cold and…" →
  "overcast" / "grey", their example), the choice is settled by a keyed
  pseudorandom function of a secret key + a few preceding words, instead of a
  fair random draw. Repeated over many low-stakes choices this leaves a
  pattern invisible to readers, detectable with the key. Implemented below
  the model layer (the model is not "aware"); a detection API is promised.
- **Quality claim:** internal testing found "no impact on the content, level
  of creativity, or readability"; cites SynthID-Text (Dathathri et al.,
  Nature 2024) human-rater studies showing no side-by-side quality
  difference.
- **Stated limitations:** heavy editing / paraphrase / third-party
  translation defeat it (Claude's own translations are watermarked); short
  passages carry too little signal; code carries less signal (low entropy per
  token — identifiers must match declarations); detection is probabilistic
  ("may have been processed by Claude"); light editing "probably won't"
  remove it, a full rewrite will.
- **Unaddressed publicly:** behavior at temperature 0 / greedy decoding;
  which token positions carry signal; key/detector specifics.

Sources: anthropic.com/news/claude-text-watermark; support.claude.com article
16266773 ("How Claude marks AI-generated content"); TechCrunch 2026-08-11 and
2026-08-15; The Register 2026-08-15.

## 2. Why this maps onto our design (the dots)

1. **Their premise is our contested quantity.** "Doesn't matter to the
   reader" is a channel-2 statement. Watermark quality evals certify channel
   2 (human raters can't tell). Our experiment measures channel 1 minus
   channel 2: whether the realized neutral choice matters to the model's own
   downstream computation when the trace is consumed as chain of thought.
   Nobody in the watermarking literature measures that; it is exactly our
   registered observable.
2. **Same operational locus.** A sampling watermark re-settles decode-time
   choices among near-equivalent candidates. Our intervention decoder does
   the same thing — uniform resample among alternatives within Δ = 1.5 nats
   of the model's realized choice, generation continuing conditioned on the
   result — restricted to reader-neutral rule sites. The randomized arm is
   functionally an aggressive, keyless watermark applied to a reasoning
   trace. Our Δ-eligibility class is a frozen, auditable version of their
   informal "low-stakes choice" class.
3. **Rule-05 is the cautionary specimen.** Rung 1's one confirmed mechanism:
   a "neutral" whitespace choice gated premature termination on the base
   checkpoint — catastrophically in multiplication:d2. Equiprobable does not
   imply inconsequential; formatting tokens can gate mechanisms (EOS
   adjacency) invisible to any reader-equivalence audit. A watermark that
   leans on whitespace or EOS-adjacent choice points could manufacture what
   looks like capability loss and is actually a termination artifact — the
   same measurement-vs-model distinction relays 6–9 adjudicated.
4. **Self-conditioning is the untested regime.** Watermark quality studies
   evaluate final outputs read by humans. Reasoning models consume their own
   watermarked tokens: CoT, multi-turn agent loops, Claude Code transcripts.
   There the watermark perturbs the model's input to later computation. Our
   depth axis (O2) is a direct probe of whether that compounds with required
   serial depth.
5. **Even "distortion-free" doesn't answer it.** Distortion-free schemes
   (Kuditipudi et al. 2023) preserve the output distribution in aggregate,
   but any watermark fixes particular realizations. Whether particular
   neutral realizations carry task state for the same model's continuation
   is orthogonal to the distortion-free guarantee — it is a property of the
   model's self-conditioning, not of the sampling distribution.

## 2b. Deployment regimes (added 2026-08-20 — Noah's downstream-of-CoT point)

Deployed watermarks today are effectively DOWNSTREAM of CoT: hidden
reasoning is pointless to mark (never delivered, so never detectable; EU
obligations cover delivered outputs), and the research frontier is
converging on answer-only marking deliberately (ReasonMark, 2601.05144,
engineered precisely to avoid perturbing the thinking phase). Which tokens
carry signal in Anthropic's deployment is undisclosed. Three-regime framing
for the paper's discussion:

1. **Answer-only (today).** The industry pays a real CAPACITY tax to sit
   here — delivered answers are often the shortest text in the exchange
   while the reasoning holds the tokens detection needs — on the strength
   of an unmeasured assumption. Our O1/O2 prices whether the tax is
   necessary: flat => reclaimable capacity inside the reader-neutral
   channel of reasoning traces; positive => the ReasonMark-style caution is
   load-bearing. (Compounding: the follow-on density result — neutral-channel
   exposure ~2.45% on instruct, unchanged from base — already says entropy
   for watermark-carrying substitutions in CoT is scarce.)
2. **Watermarked reasoning (unstable boundary).** Capacity pressure pushes
   vendors toward marking the longest text available. If visible/delivered
   reasoning gets marked, our measurement applies directly.
3. **Agentic self-consumption (already here).** "Downstream of CoT" holds
   for ONE turn only. Watermarked output re-entering a context window —
   agents reading their own prior turns, distillation, model-quoting-model —
   makes today's watermark upstream of tomorrow's reasoning. No vendor
   quality eval covers iterated self-consumption; our
   perturb-then-condition topology is a direct model of it, depth axis
   included.

Plus the termination caveat that regime 1 is not free: rung 1's confirmed
rule-05 mechanism operated at the END of the trace — EOS-adjacent,
answer-region territory. Answer-only marking that touches formatting near
the close of generation plays with exactly that channel.

## 3. Honest asymmetries (must appear wherever the connection is drawn)

- **Dose.** Ours is harsher: uniform resampling within the eligibility class
  (worst case within class, every matched site), versus a soft keyed bias
  among candidates the model already rated plausible. A positive result for
  us does NOT automatically condemn watermarking — dose matters.
- **Direction of reassurance is asymmetric.** A flat result under our
  harsher perturbation is STRONGER reassurance for watermarking CoT than
  watermark-strength evidence would be. A positive result is a caution
  flag that says "measure before watermarking reasoning," not "watermarking
  breaks reasoning."
- **Site coverage differs.** Watermarks touch any low-stakes position;
  our rules touch only pre-registered reader-neutral classes with protected
  channel 2 (ordering, granularity, hedging untouched). Ours is narrower and
  cleaner; theirs is broader and uncharacterized.
- **Scale and stack.** One 7B open-weights model, greedy decoding, three
  synthetic task families. Rung 1 bounds this regime, not the phenomenon.
- **Entropy overlap caveat.** Greedy-ish instruct CoT is low-entropy, so
  watermark signal in reasoning traces is weak to begin with (their own code
  caveat generalizes) — the same exposure-collapse that bit rung 1's grid.
  Both facts cut the same way: fewer genuinely free choices in CoT than in
  prose.

## 4. Framing plan per output

- **Pre-registration post (LessWrong):** UNCHANGED. It is frozen-time text
  timestamped by the manifest hash; retrofitting motivation into it would
  undercut the very property that makes it valuable. The announcement
  postdating the freeze is the selling point — say so in the results post,
  not the prereg post.
- **Results post (LessWrong, published together with the prereg post):**
  Lead or near-lead with the watermarking hook: "Five days after we froze
  [the follow-on grid], Anthropic announced watermarking built on the
  assumption our experiment tests." Structure: the assumption ("doesn't
  matter to the reader") → our measurement of the model-side version → what
  we found → what it means for watermarking reasoning traces, with the §3
  asymmetries stated plainly. Rule-05 termination is the concrete,
  explainable-to-anyone example either way.
- **Paper:** Intro gains the deployed-application motivation (regulation-
  driven, industry-wide, no opt-out — the assumption is now load-bearing at
  scale). Related Work gains a watermarking paragraph: Kirchenbauer et al.
  2023 (arXiv:2301.10226), Aaronson's Gumbel scheme, Kuditipudi et al. 2023
  (arXiv:2307.15593), SynthID-Text (Dathathri et al., Nature 2024),
  Anthropic deployment 2026 — framed as "quality evals certify
  reader-equivalence; we measure model-equivalence." Discussion maps O1/O2
  outcomes to watermark-CoT safety per §3. Add all to references.bib.
- **Outcome-conditional lines (both must be pre-drafted, per the additivity
  discipline in positioning_notes.md):**
  - Flat interaction: first measured upper bound on the cost of re-settling
    reader-neutral choices in CoT under perturbation strictly harsher than a
    sampling watermark — direct, quantified support for extending the
    "no quality impact" claim to self-consumed reasoning text at this scale,
    with the termination-channel warning label attached.
  - Positive interaction: evidence that neutral-choice perturbation taxes
    deep reasoning specifically — i.e., watermark-induced degradation would
    concentrate exactly where models most need their CoT, and "no visible
    quality difference" evals would systematically miss it.

## 5. Operational consequences for this repo

1. **Generation side: unaffected.** Local Qwen checkpoints, greedy decoding,
   no Anthropic model in the generation loop, nothing watermarked enters the
   experiment's traces.
2. **Judge determinism check (required, before audit phase).** The frozen
   judge is claude-opus-4-5-20251101 at temperature 0 (environment.json).
   Older models are being retrofitted "over the coming months," and
   Anthropic has not said how watermarking interacts with temperature 0. If
   the serving stack starts re-settling near-argmax ties with a keyed
   function, pinned-judge outputs could drift. Action: re-run the judge
   smoke test (JUDGE_SMOKE_TEST.json) immediately before the audit phase; if
   outputs are not reproduced, treat as an environment break under FREEZE.md
   and consult both parties before auditing. Cost: pennies. Log the result
   either way.
3. **Disclosure line for posts/paper:** prose drafted with Claude's help
   will itself carry Claude's watermark. The collaboration is already
   disclosed prominently (it is the headline of the design); one sentence
   noting the recursion is honest and, frankly, good copy.
4. **Key rotation reminder:** the pre-paper deadline for rotating the
   Anthropic + RunPod keys (REVIEW_NOTES deferred item) now also predates
   any judge re-verification runs.
