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
  PROBS="runs/problems/main-$CELL.jsonl"
  if [ -s "$OUT" ] && [ "$(wc -l < "$OUT")" -eq "$(wc -l < "$PROBS")" ]; then
    echo "[skip] $OUT complete"
    continue
  fi
  # Partial output from an interrupted run: redo the cell from scratch so
  # the record set is exactly the problem set (runner appends per record).
  rm -f "$OUT"
  echo "[run] $LABEL / $CELL"
  # Model pin + extra flags are env-overridable so the pre-registered
  # follow-on (instruct pin, 8.1(b) measurement flags) reuses this script;
  # defaults are byte-identical to the rung 1 invocation.
  python -m harness.runner \
    --model-id "${PASS_MODEL_ID:-Qwen/Qwen2.5-7B}" \
    --revision "${PASS_REVISION:-d149729398750b98c0af14eb82c78cfe92750796}" \
    --device cuda --dtype bfloat16 \
    --problems "runs/problems/main-$CELL.jsonl" \
    --mode "$PASS_MODE" $RULES_ARG \
    --seed "$PASS_SEED" \
    --max-new-tokens 1024 \
    ${PASS_EXTRA_ARGS:-} \
    --out "$OUT" >> "runs/$LABEL.log" 2>&1
done
echo "[done] $LABEL"
