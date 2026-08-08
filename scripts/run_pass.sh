#!/bin/bash
# Run ONE main-run pass (a mode x rules x seed combination) over a cell list.
# Parameter-driven; the ruled grid/n/seeds are supplied by the caller so this
# script encodes no party decisions.
#
# Usage:
#   PASS_MODE=native        PASS_SEED=271828 ./scripts/run_pass.sh reachability-d2 ...
#   PASS_MODE=randomized    PASS_SEED=271828 ./scripts/run_pass.sh <cells...>
#   PASS_MODE=randomized PASS_RULES=tier_a_01_connectives PASS_SEED=161803 ./scripts/run_pass.sh <cells...>
#
# Cells are basenames of runs/problems/main-<cell>.jsonl (e.g. reachability-d2).
# Output: runs/<pass-label>/<cell>.jsonl ; log: runs/<pass-label>.log
set -euo pipefail
cd "$(dirname "$0")/.."

: "${PASS_MODE:?native|randomized}"
: "${PASS_SEED:?intervention seed}"
RULES_ARG=""
LABEL="$PASS_MODE-all-s$PASS_SEED"
if [ "${PASS_RULES:-}" != "" ]; then
  RULES_ARG="--rules $PASS_RULES"
  LABEL="$PASS_MODE-$PASS_RULES-s$PASS_SEED"
fi
if [ "$PASS_MODE" = "native" ]; then
  LABEL="native"
fi

mkdir -p "runs/$LABEL"
for CELL in "$@"; do
  OUT="runs/$LABEL/$CELL.jsonl"
  if [ -s "$OUT" ]; then
    echo "[skip] $OUT exists"
    continue
  fi
  echo "[run] $LABEL / $CELL"
  python -m harness.runner \
    --model-id Qwen/Qwen2.5-7B \
    --revision d149729398750b98c0af14eb82c78cfe92750796 \
    --device cuda --dtype bfloat16 \
    --problems "runs/problems/main-$CELL.jsonl" \
    --mode "$PASS_MODE" $RULES_ARG \
    --seed "$PASS_SEED" \
    --max-new-tokens 1024 \
    --out "$OUT" >> "runs/$LABEL.log" 2>&1
done
echo "[done] $LABEL"
