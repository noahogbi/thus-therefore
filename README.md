# cot-freeze — Neutral-Choice Randomization Experiment

A pre-registered experiment testing whether LLM chain-of-thought carries covert task
state in reader-neutral token choices. Design was frozen in an adversarial dialogue
between two frontier models (Fable / Sol) with opposing registered predictions; this
repo implements it. Nature decides who pays.

## Quick start (new machine)

```bash
unzip cot-freeze.zip && cd cot-freeze
git init && git add -A && git commit -m "frozen spec import"
python3 tasks/generate_tasks.py --family composition --depth 6 --n 5 --seed 1337 --out /tmp/smoke.jsonl
```

If the smoke test prints "wrote 5 problems", the frozen parts work. Everything else
is built in `harness/`.

## Read in this order

| File | What it is |
|---|---|
| **CLAUDE.md** | Standing instructions for Claude Code — auto-loaded every session |
| **HANDOFF.md** | Build plan: what's frozen, what to build, in what order |
| **SPEC.md** | The frozen experimental design (normative — wins all conflicts) |
| **FREEZE.md** | Amendment/validation/hashing protocol |
| `rules/tier_a/` | Seven frozen intervention rule tables (JSON) |
| `rules/disputed/` | Four separate-arm cells with both parties' predictions |
| `tasks/generate_tasks.py` | Depth-parametrized problem generator (working) |
| `judge/judge_prompt.txt` | Frozen post-hoc audit prompt |
| `scripts/hash_commit.py` | Generates FREEZE_MANIFEST.json before any run |

## One-paragraph experiment summary

Decode greedily everywhere except at pre-registered sites where the model chose among
reader-equivalent surface forms (thus/therefore, x=17 / x = 17, ...). At those sites,
sample uniformly among alternatives within 1.5 nats of the model's preferred choice.
If apparently irrelevant wording is carrying recurrent computational state, this
randomization should increasingly damage accuracy as required serial reasoning depth
grows (Sol's prediction). If the readable semantics carry the load, the penalty
should be flat-to-zero in depth on base/light-instruct models (Fable's prediction),
emerging only after outcome-filtered training. Both predictions are registered in
SPEC.md section 6 and cannot be revised after data.

## Status

- [x] Design frozen (2026-08-06)
- [x] Tier A rule tables drafted; adversarial review COMPLETE — findings ruled on by both parties, dispositions applied (REVIEW_LOG.md, 2026-08-07); rule 02 display-line set amended (F2); rule 03 sequencing set structurally disabled in code (F1)
- [ ] environment.json pinned — DRAFT complete incl. party-ruled judge (claude-opus-4-5-20251101, temp 0, thinking omitted); judge smoke test PENDING (requires API key; Sol's F3 condition)
- [ ] Harness: matcher DONE; eligibility scorer DONE (F5 two-region scoring, Δ=1.5); intervention decoder + density logger DONE (95 tests total, incl. HF-adapter integration tests against pinned transformers 5.14.1); depth calibrator + audit sampler pending; see REVIEW_LOG IN-1 for a decoder-side conservative rule awaiting party awareness
- [ ] Matcher-only review pass: dry run regenerated post-amendment (24 traces, 298 sites); Noah's Step 4 sign-off PENDING
- [ ] seeds.json completed, FREEZE_MANIFEST.json generated and published
- [ ] Depth calibration (native greedy, with/without trace)
- [ ] Main run (native vs. neutral-randomized)
- [ ] Audit + analysis (O1 raw penalty, O2 depth interaction, per rule)

## Hardware

Rented RTX 4090 (24GB) on Vast.ai / RunPod (~$0.30–0.50/hr). Local: harness
development, task generation, matcher tests, probe training, analysis — all CPU-fine.
GPU needed only for eligibility scoring, generation runs, and (later) LoRA work.
