# RUNBOOK — phase entry points

One command per phase (CLAUDE.md session hygiene). All phases after the
freeze REQUIRE the published FREEZE_MANIFEST; nothing below except setup and
smoke tests may run before `scripts/hash_commit.py` output is committed.

## GPU box setup (rented RTX 4090, via SSH)

```bash
git clone https://github.com/noahogbi/thus-therefore && cd thus-therefore
pip install "transformers==5.14.1" torch  # match environment.json pin
python -m pytest tests/ -q                # all 114 must pass
python tasks/generate_tasks.py --family composition --depth 6 --n 5 --seed 1337 --out /tmp/smoke.jsonl
```

## Phase 0 — judge smoke test (pre-hash, Sol's F3 condition; needs ANTHROPIC_API_KEY)

```bash
python scripts/judge_smoke_test.py
```

## Phase 1 — task generation (frozen generator; seeds from seeds.json)

```bash
for FAM in multiplication composition reachability; do
  for D in 2 4 6 8 10; do
    python tasks/generate_tasks.py --family $FAM --depth $D --n 200 \
      --seed 1337 --out runs/problems/$FAM-d$D.jsonl
  done
done
```

(Depth grid above is illustrative — the real grid is chosen AFTER phase 2.)

## Phase 2 — depth calibration (native greedy only)

```bash
python -m harness.calibrate \
  --model-id Qwen/Qwen2.5-7B --revision d149729398750b98c0af14eb82c78cfe92750796 \
  --device cuda --dtype bfloat16 \
  --problems runs/problems/*.jsonl --out runs/calibration.json
```

Pick the (family, depth) cells with large with/without-trace gaps; that grid
is the depth axis for the main run.

## Phase 3 — main run (per arm)

Native control arm (once per problem set):

```bash
python -m harness.runner --model-id Qwen/Qwen2.5-7B \
  --revision d149729398750b98c0af14eb82c78cfe92750796 \
  --problems runs/problems/<cell>.jsonl --mode native --seed <intervention_sampling_seed> \
  --out runs/native/<cell>.jsonl
```

Randomized arms — all-rules aggregate and/or per-rule (arm plan decided with
the parties before GPU spend):

```bash
python -m harness.runner ... --mode randomized --seed <intervention_sampling_seed> \
  --out runs/rand-all/<cell>.jsonl
python -m harness.runner ... --mode randomized --rules tier_a_01_connectives \
  --seed <intervention_sampling_seed> --out runs/rand-r01/<cell>.jsonl
```

## Phase 4 — audit (BEFORE any outcome analysis)

```bash
python -m harness.audit --runs runs/rand-*/*.jsonl \
  --seed <audit_sample_seed> --n 500 \
  --items-out runs/audit_items.jsonl --key-out runs/audit_key.jsonl
```

Judge the items with the pinned judge (environment.json), join verdicts to
the key file, compute the frozen per-rule 98% threshold. A failing rule is
removed WHOLE and the experiment rerun under a new hash (FREEZE.md item 7).

## Phase 5 — analysis (only after the audit)

```bash
python -m harness.analysis --arm-label tier_a_all \
  --native runs/native/*.jsonl --randomized runs/rand-all/*.jsonl \
  --out runs/analysis-all.json
```

One invocation per arm. Disputed cells are separate arms and are NEVER
pooled with Tier A (frozen reporting policy).
