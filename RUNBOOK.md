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

RULED GRID (third consultation, both parties, 2026-08-08): cells =
reachability d2/d4/d6/d8 + multiplication d2 + composition d2; n = 400 per
cell; problem generation seed 2026 (calibration used 1337). Generate:

```bash
mkdir -p runs/problems
for CELL in "reachability 2" "reachability 4" "reachability 6" "reachability 8" \
            "multiplication 2" "composition 2"; do
  set -- $CELL
  python tasks/generate_tasks.py --family $1 --depth $2 --n 400 --seed 2026 \
    --out runs/problems/main-$1-d$2.jsonl
done
```

Passes are executed via scripts/run_pass.sh (idempotent per cell; safe to
re-run after interruption). 25 passes total: native + (aggregate + 7 rules)
x 3 seeds. Arms are independent — split passes across parallel pods.


Arm plan (ruled 2b by both parties, REVIEW_LOG second reconciliation):
native control + Tier A aggregate arm + all seven per-rule arms, with the
SAME three intervention seeds (271828, 161803, 141421) on every randomized
arm. The aggregate arm is the primary test of the section 6 predictions;
per-rule arms are the registered decomposition and are never selectively
promoted post hoc.

Native control arm (once per problem set):

```bash
python -m harness.runner --model-id Qwen/Qwen2.5-7B \
  --revision d149729398750b98c0af14eb82c78cfe92750796 \
  --problems runs/problems/<cell>.jsonl --mode native --seed 271828 \
  --out runs/native/<cell>.jsonl
```

Randomized arms — aggregate plus each rule in isolation, times three seeds:

```bash
for SEED in 271828 161803 141421; do
  python -m harness.runner ... --mode randomized --seed $SEED \
    --out runs/rand-all/s$SEED-<cell>.jsonl
  for RULE in tier_a_01_connectives tier_a_02_punctuation \
      tier_a_03_discourse_markers tier_a_04_contractions \
      tier_a_05_whitespace tier_a_06_operator_spacing tier_a_07_list_markers; do
    python -m harness.runner ... --mode randomized --rules $RULE --seed $SEED \
      --out runs/rand-$RULE/s$SEED-<cell>.jsonl
  done
done
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
