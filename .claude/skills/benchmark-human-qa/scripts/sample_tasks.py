#!/usr/bin/env python3
"""Select a reproducible random sample of benchmark tasks."""

from __future__ import annotations

import argparse
import json
import math
import random
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sample a reproducible subset of benchmark tasks.",
    )
    parser.add_argument(
        "--tasks-root",
        default="benchmark/tasks",
        help="Root directory containing task folders.",
    )
    parser.add_argument(
        "--fraction",
        type=float,
        default=0.10,
        help="Fraction of tasks to sample.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed. Defaults to local date as YYYYMMDD.",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=1,
        help="Minimum number of tasks to sample.",
    )
    parser.add_argument(
        "--output",
        help="Optional JSON file to write the manifest to.",
    )
    return parser.parse_args()


def default_seed() -> int:
    return int(datetime.now().strftime("%Y%m%d"))


def discover_tasks(tasks_root: Path) -> list[str]:
    task_ids: list[str] = []
    for child in sorted(tasks_root.iterdir()):
        if child.is_dir() and (child / "task.yaml").exists():
            task_ids.append(child.name)
    return task_ids


def main() -> int:
    args = parse_args()
    seed = args.seed if args.seed is not None else default_seed()

    tasks_root = Path(args.tasks_root)
    if not tasks_root.exists():
        raise SystemExit(f"Task root does not exist: {tasks_root}")

    task_ids = discover_tasks(tasks_root)
    if not task_ids:
        raise SystemExit(f"No tasks found under: {tasks_root}")

    count = max(args.min_count, math.ceil(len(task_ids) * args.fraction))
    count = min(count, len(task_ids))

    rng = random.Random(seed)
    selected = sorted(rng.sample(task_ids, count))

    manifest = {
        "tasks_root": str(tasks_root),
        "total_task_count": len(task_ids),
        "sample_fraction": args.fraction,
        "sample_count": count,
        "seed": seed,
        "selected_tasks": selected,
    }

    payload = json.dumps(manifest, indent=2) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload)

    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
