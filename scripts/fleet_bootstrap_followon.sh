#!/bin/bash
# Follow-on (instruct) main-run fleet worker. Args: POD_ID then pass specs
# "MODE:RULES:SEED" executed in order, e.g.
#   fleet_bootstrap_followon.sh <pod-id> native:-:271828 randomized:all:271828
# Idempotent (run_pass.sh skips completed cells); stops the pod when done.
#
# Encodes the ninth-relay ruling (unanimous 9.1(c)): union grid = rung 1's
# six cells + reachability:10 + composition:4, n=400, generation seed 2026.
# Measurement per the 8.1(b) amendment (manifest 5bcf4dc8): extended
# extraction + terminal set {configured EOS, <|endoftext|>}; prompt bytes
# unchanged (same generator, same seed as rung 1).
set -euo pipefail
POD_ID="$1"; shift
SPECS=("$@")   # save BEFORE any `set --` clobbers the positional params
cd /workspace
if [ ! -d thus-therefore ]; then git clone -q https://github.com/noahogbi/thus-therefore.git; fi
cd thus-therefore
git pull -q || true
pip install -q "transformers==5.14.1" pytest 2>&1 | tail -1 || true

mkdir -p runs/problems
for CELL in "reachability 2" "reachability 4" "reachability 6" "reachability 8" \
            "reachability 10" "multiplication 2" "composition 2" "composition 4"; do
  set -- $CELL
  F="runs/problems/main-$1-d$2.jsonl"
  [ -s "$F" ] || python tasks/generate_tasks.py --family "$1" --depth "$2" \
    --n 400 --seed 2026 --out "$F"
done

CELLS="reachability-d2 reachability-d4 reachability-d6 reachability-d8 reachability-d10 multiplication-d2 composition-d2 composition-d4"
export PASS_MODEL_ID="Qwen/Qwen2.5-7B-Instruct"
export PASS_REVISION="a09a35458c702b33eeacc393d103063234e8bc28"
export PASS_EXTRA_ARGS="--extended-extraction --extra-terminal-token <|endoftext|>"
for SPEC in "${SPECS[@]}"; do
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
runpodctl stop pod "$POD_ID" || true
