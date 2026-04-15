#!/usr/bin/env python3
"""Compare human and browser-use benchmark run artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare human and browser-use run artifacts.",
    )
    parser.add_argument("human_dir", help="Run directory for the human episode.")
    parser.add_argument(
        "browser_use_dir",
        help="Run directory for the browser-use episode.",
    )
    parser.add_argument("--output", help="Optional JSON file to write.")
    return parser.parse_args()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def canonicalize_diff(entries: list[dict]) -> list[dict]:
    return sorted(
        entries,
        key=lambda item: (
            item.get("model"),
            json.dumps(item.get("entity_key"), sort_keys=True),
            item.get("field"),
            item.get("op"),
            json.dumps(item.get("norm_value"), sort_keys=True),
        ),
    )


def summarize_run(run_dir: Path) -> dict[str, Any]:
    score = load_json(run_dir / "score.json", {})
    postconditions = load_json(run_dir / "postcondition_failures.json", [])
    agent_result = load_json(run_dir / "agent_result.json", {})
    state_diff = load_json(run_dir / "state_diff.json", [])
    return {
        "run_dir": str(run_dir),
        "outcome_success": score.get("outcome_success"),
        "strict_success": score.get("strict_success"),
        "gave_up": score.get("gave_up", agent_result.get("gave_up")),
        "wall_clock_sec": score.get("wall_clock_sec"),
        "matching_edits": score.get("matching_edits"),
        "missing_edits": score.get("missing_edits"),
        "extra_edits": score.get("extra_edits"),
        "postcondition_failures": postconditions,
        "postcondition_failure_count": len(postconditions),
        "returncode": agent_result.get("returncode"),
        "reason": agent_result.get("reason"),
        "state_diff": canonicalize_diff(state_diff),
    }


def main() -> int:
    args = parse_args()
    human_dir = Path(args.human_dir)
    browser_dir = Path(args.browser_use_dir)

    human = summarize_run(human_dir)
    browser_use = summarize_run(browser_dir)

    comparison = {
        "human": {k: v for k, v in human.items() if k != "state_diff"},
        "browser_use": {k: v for k, v in browser_use.items() if k != "state_diff"},
        "same_outcome_success": human["outcome_success"] == browser_use["outcome_success"],
        "same_strict_success": human["strict_success"] == browser_use["strict_success"],
        "same_postcondition_failures": (
            human["postcondition_failures"] == browser_use["postcondition_failures"]
        ),
        "same_state_diff": human["state_diff"] == browser_use["state_diff"],
        "human_passes_task": bool(human["outcome_success"]),
        "browser_use_passes_task": bool(browser_use["outcome_success"]),
    }

    payload = json.dumps(comparison, indent=2) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload)

    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
