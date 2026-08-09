#!/bin/bash
# Main-run fleet worker. Args: pass specs "MODE:RULES:SEED" executed in
# order, e.g.  native:-:271828  randomized:all:271828
# randomized:tier_a_06_operator_spacing:161803
# Idempotent (run_pass.sh skips completed cells); stops the pod when done.
set -euo pipefail
cd /workspace/thus-therefore
git pull -q || true
pip install -q "transformers==5.14.1" pytest 2>&1 | tail -1 || true

# Ruled grid (third consultation): n=400, generation seed 2026.
mkdir -p runs/problems
for CELL in "reachability 2" "reachability 4" "reachability 6" "reachability 8" \
            "multiplication 2" "composition 2"; do
  set -- $CELL
  F="runs/problems/main-$1-d$2.jsonl"
  [ -s "$F" ] || python tasks/generate_tasks.py --family "$1" --depth "$2" \
    --n 400 --seed 2026 --out "$F"
done

CELLS="reachability-d2 reachability-d4 reachability-d6 reachability-d8 multiplication-d2 composition-d2"
for SPEC in "$@"; do
  MODE="${SPEC%%:*}"; REST="${SPEC#*:}"; RULES="${REST%%:*}"; SEED="${REST#*:}"
  export PASS_MODE="$MODE" PASS_SEED="$SEED"
  if [ "$RULES" != "all" ] && [ "$RULES" != "-" ]; then
    export PASS_RULES="$RULES"
  else
    unset PASS_RULES || true
  fi
  echo "=== pass $SPEC start $(date -u +%H:%M:%S) ==="
  bash scripts/run_pass.sh $CELLS
done
echo "=== all passes done $(date -u +%H:%M:%S) ==="
runpodctl stop pod "$RUNPOD_POD_ID"
