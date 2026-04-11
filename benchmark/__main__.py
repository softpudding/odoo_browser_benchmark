"""CLI entry point for the Odoo browser agent benchmark.

Usage::

    python -m benchmark list                         # list all tasks
    python -m benchmark show <task_id>               # show task details
    python -m benchmark score <run_dir>              # re-score a completed run
    python -m benchmark run <task_dir> [--output-dir DIR]  # run a task (requires agent + Odoo)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


def cmd_list(args: argparse.Namespace) -> None:
    """List all available benchmark tasks."""
    tasks_dir = pathlib.Path(__file__).parent / "tasks"
    if not tasks_dir.exists():
        print("No tasks directory found.")
        return

    for task_dir in sorted(tasks_dir.iterdir()):
        task_file = task_dir / "task.yaml"
        if task_file.exists():
            import yaml
            task = yaml.safe_load(task_file.read_text())
            difficulty = task.get("difficulty", "?")
            module = task.get("module", "?")
            print(f"  {task.get('task_id', task_dir.name):<50s}  "
                  f"module={module:<30s}  difficulty={difficulty}")


def cmd_show(args: argparse.Namespace) -> None:
    """Show details of a specific task."""
    from benchmark.schema import load_task, task_to_dict

    task_dir = _resolve_task_dir(args.task_id)
    if task_dir is None:
        print(f"Task not found: {args.task_id}", file=sys.stderr)
        sys.exit(1)

    task = load_task(task_dir)
    print(json.dumps(task_to_dict(task), indent=2, default=str))


def cmd_score(args: argparse.Namespace) -> None:
    """Re-score a completed run from its artifacts."""
    from benchmark.runners.score_task import TaskScorer
    from benchmark.schema import load_task

    run_dir = pathlib.Path(args.run_dir)
    task_dir = _resolve_task_dir(args.task_id)
    if task_dir is None:
        print(f"Task not found: {args.task_id}", file=sys.stderr)
        sys.exit(1)

    task = load_task(task_dir)

    # Load artifacts
    trace = json.loads((run_dir / "trace.json").read_text())
    state_diff = json.loads((run_dir / "state_diff.json").read_text())

    expected_path = run_dir / "expected_state.json"
    expected_diff = json.loads(expected_path.read_text()) if expected_path.exists() else []

    pc_path = run_dir / "postcondition_failures.json"
    postcondition_failures = json.loads(pc_path.read_text()) if pc_path.exists() else []

    # Load original metrics and agent state from saved artifacts
    orig_score_path = run_dir / "score.json"
    orig_score = json.loads(orig_score_path.read_text()) if orig_score_path.exists() else {}

    agent_result_path = run_dir / "agent_result.json"
    agent_result = json.loads(agent_result_path.read_text()) if agent_result_path.exists() else {}

    artifacts = {
        "trace": trace,
        "state_diff": state_diff,
        "expected_diff": expected_diff,
        "postcondition_failures": postcondition_failures,
        "gave_up": agent_result.get("gave_up", False),
        "wall_clock_sec": orig_score.get("wall_clock_sec", 0.0),
        "browser_step_count": orig_score.get("browser_step_count", 0),
        "token_cost": orig_score.get("token_cost"),
    }

    scorer = TaskScorer(task, artifacts)
    result = scorer.score()
    print(json.dumps(result.to_dict(), indent=2))


def cmd_run(args: argparse.Namespace) -> None:
    """Placeholder for running a task (requires Odoo + Playwright)."""
    print("To run a benchmark task, use the TaskRunner API directly:")
    print()
    print("    from benchmark.runners.run_task import TaskRunner")
    print(f"    runner = TaskRunner('{args.task_dir}')")
    print("    result = runner.run(agent_fn=my_agent, odoo_env=env, page=page)")
    print()
    print("See benchmark/runners/run_task.py for the full API.")


def _resolve_task_dir(task_id: str) -> pathlib.Path | None:
    """Resolve a task_id to its directory."""
    tasks_dir = pathlib.Path(__file__).parent / "tasks"

    # Direct match
    direct = tasks_dir / task_id
    if direct.exists():
        return direct

    # Search by task_id in task.yaml files
    import yaml
    for candidate in tasks_dir.iterdir():
        task_file = candidate / "task.yaml"
        if task_file.exists():
            task = yaml.safe_load(task_file.read_text())
            if task.get("task_id") == task_id:
                return candidate

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="benchmark",
        description="Odoo Backend-Grounded Browser Agent Benchmark",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all benchmark tasks")

    show_p = sub.add_parser("show", help="Show task details")
    show_p.add_argument("task_id", help="Task ID or directory name")

    score_p = sub.add_parser("score", help="Re-score a completed run")
    score_p.add_argument("task_id", help="Task ID")
    score_p.add_argument("run_dir", help="Directory containing run artifacts")

    run_p = sub.add_parser("run", help="Run a benchmark task")
    run_p.add_argument("task_dir", help="Task directory path")
    run_p.add_argument("--output-dir", help="Output directory for artifacts")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "score":
        cmd_score(args)
    elif args.command == "run":
        cmd_run(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
