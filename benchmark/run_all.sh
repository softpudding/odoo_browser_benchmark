#!/bin/bash
# Run all benchmark tasks with a specified agent.
#
# Each task auto-isolates (own DB, port, Odoo process) so tasks can
# run in parallel with --parallel N.
#
# Usage:
#   ./benchmark/run_all.sh                          # browser-use, serial
#   ./benchmark/run_all.sh --parallel 4             # 4 tasks concurrently
#   ./benchmark/run_all.sh --agent human            # human eval
#   ./benchmark/run_all.sh --provider dashscope     # use dashscope
#   ./benchmark/run_all.sh --task sale.confirm_correct_order  # single task
#   ./benchmark/run_all.sh --primary-track          # only curated hard cases

set -euo pipefail
cd "$(dirname "$0")/.."

# Load API keys
eval "$(grep BROWSER_USE_API_KEY ~/.zshrc 2>/dev/null || true)"
eval "$(grep DASHSCOPE_API_KEY ~/.zshrc 2>/dev/null || true)"

# Defaults
AGENT="browser-use"
PROVIDER="browser-use"
MAX_STEPS=""
HEADED="--headed"
SINGLE_TASK=""
PRIMARY_ONLY=0
PARALLEL=1
EXTRA_ARGS=""

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent)      AGENT="$2"; shift 2 ;;
        --provider)   PROVIDER="$2"; shift 2 ;;
        --max-steps)  MAX_STEPS="$2"; shift 2 ;;
        --headless)   HEADED="--headless"; shift ;;
        --task)       SINGLE_TASK="$2"; shift 2 ;;
        --primary-track) PRIMARY_ONLY=1; shift ;;
        --parallel)   PARALLEL="$2"; shift 2 ;;
        *)            EXTRA_ARGS="$EXTRA_ARGS $1"; shift ;;
    esac
done

# All tasks
ALL_TASKS=()
if [[ $PRIMARY_ONLY -eq 1 ]]; then
    while IFS= read -r task; do
        ALL_TASKS+=("$task")
    done < <(
        python3 - <<'PY'
from pathlib import Path
import yaml

for task_dir in sorted(Path("benchmark/tasks").iterdir()):
    task_file = task_dir / "task.yaml"
    if not task_file.exists():
        continue
    task = yaml.safe_load(task_file.read_text()) or {}
    metadata = task.get("metadata") or {}
    if metadata.get("primary_track"):
        print(task.get("task_id", task_dir.name))
PY
    )
else
    while IFS= read -r task; do
        ALL_TASKS+=("$task")
    done < <(
        find benchmark/tasks -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
    )
fi

# Filter to single task if specified
if [[ -n "$SINGLE_TASK" ]]; then
    ALL_TASKS=("$SINGLE_TASK")
fi

echo "=========================================="
echo "  Benchmark Run: agent=$AGENT provider=$PROVIDER parallel=$PARALLEL"
echo "  Tasks: ${ALL_TASKS[*]}"
echo "=========================================="
echo ""

MAX_STEPS_ARG=""
if [[ -n "$MAX_STEPS" ]]; then
    MAX_STEPS_ARG="--max-steps $MAX_STEPS"
fi

if [[ $PARALLEL -gt 1 ]]; then
    # Parallel mode: use xargs -P to run tasks concurrently.
    # Each eval.py run auto-isolates (own DB, port, Odoo process).
    RESULTS_DIR=$(mktemp -d /tmp/bench_results_XXXXXX)

    run_one_task() {
        local task="$1"
        local log_file="$RESULTS_DIR/${task}.log"
        echo "[START] $task"
        if uv run benchmark-eval run "$task" \
            --agent "$AGENT" \
            --provider "$PROVIDER" \
            $MAX_STEPS_ARG \
            $HEADED \
            $EXTRA_ARGS \
            > "$log_file" 2>&1; then
            if grep -q "RESULT: PASS" "$log_file"; then
                echo "[PASS]  $task"
                echo "PASS" > "$RESULTS_DIR/${task}.status"
            else
                echo "[FAIL]  $task"
                echo "FAIL" > "$RESULTS_DIR/${task}.status"
            fi
        else
            echo "[FAIL]  $task"
            echo "FAIL" > "$RESULTS_DIR/${task}.status"
        fi
    }
    export -f run_one_task
    export RESULTS_DIR AGENT PROVIDER MAX_STEPS_ARG HEADED EXTRA_ARGS

    printf '%s\n' "${ALL_TASKS[@]}" | xargs -P "$PARALLEL" -I{} bash -c 'run_one_task "$@"' _ {}

    # Aggregate results
    PASS=0
    FAIL=0
    RESULTS=""
    for task in "${ALL_TASKS[@]}"; do
        status=$(cat "$RESULTS_DIR/${task}.status" 2>/dev/null || echo "FAIL")
        if [[ "$status" == "PASS" ]]; then
            PASS=$((PASS + 1))
            RESULTS="$RESULTS\n  PASS  $task"
        else
            FAIL=$((FAIL + 1))
            RESULTS="$RESULTS\n  FAIL  $task"
        fi
        # Show key metrics from log
        if [[ -f "$RESULTS_DIR/${task}.log" ]]; then
            echo ""
            echo "--- $task ---"
            grep -E "RESULT|StateDiff|Strict|WritePrecision|HarmfulWrite|Writes:|Forbidden|Required ops|Wall clock|Missing|Extra|Postcondition" "$RESULTS_DIR/${task}.log" || true
        fi
    done

    rm -rf "$RESULTS_DIR"
else
    # Serial mode (original behaviour)
    PASS=0
    FAIL=0
    RESULTS=""

    for task in "${ALL_TASKS[@]}"; do
        echo ""
        echo "=============================================="
        echo "  TASK: $task"
        echo "=============================================="

        CMD="uv run benchmark-eval run $task \
            --agent $AGENT \
            --provider $PROVIDER \
            $MAX_STEPS_ARG \
            $HEADED \
            $EXTRA_ARGS"

        if OUTPUT=$(eval "$CMD" 2>&1); then
            CMD_STATUS=0
        else
            CMD_STATUS=$?
        fi

        echo "$OUTPUT" | grep -E "RESULT|StateDiff|Strict|WritePrecision|HarmfulWrite|Writes:|Forbidden|Required ops|Wall clock|Missing|Extra|Postcondition" || true

        # Track pass/fail
        if [[ $CMD_STATUS -eq 0 ]] && echo "$OUTPUT" | grep -q "RESULT: PASS"; then
            PASS=$((PASS + 1))
            RESULTS="$RESULTS\n  PASS  $task"
        else
            FAIL=$((FAIL + 1))
            RESULTS="$RESULTS\n  FAIL  $task"
        fi
    done
fi

echo ""
echo "=============================================="
echo "  SUMMARY: $PASS passed, $FAIL failed"
echo "=============================================="
echo -e "$RESULTS"
echo ""
