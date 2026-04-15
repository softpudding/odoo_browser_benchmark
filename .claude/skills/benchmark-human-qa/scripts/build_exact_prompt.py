#!/usr/bin/env python3
"""Build the exact browser-use instruction block for a benchmark task."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the exact browser-use prompt for a benchmark task.",
    )
    parser.add_argument("task_id", help="Task id or path to task directory.")
    parser.add_argument("--base-url", required=True, help="Base URL for the run.")
    parser.add_argument("--db", required=True, help="Database name for the run.")
    parser.add_argument("--login", help="Login override.")
    parser.add_argument("--password", help="Password override.")
    return parser.parse_args()


def resolve_task_dir(task_id: str) -> Path:
    candidate = Path(task_id)
    if candidate.exists():
        return candidate.resolve()
    resolved = REPO_ROOT / "benchmark" / "tasks" / task_id
    if resolved.exists():
        return resolved
    raise SystemExit(f"Task directory not found for: {task_id}")


def load_browser_use_module():
    module_path = REPO_ROOT / "setup" / "browser_use_local.py"
    spec = importlib.util.spec_from_file_location("browser_use_local", module_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_task(task_dir: Path) -> tuple[dict, str]:
    task_yaml = yaml.safe_load((task_dir / "task.yaml").read_text())
    prompt = (task_dir / "prompt.md").read_text().strip()
    return task_yaml, prompt


def main() -> int:
    args = parse_args()
    task_dir = resolve_task_dir(args.task_id)
    task, instruction = load_task(task_dir)

    login_context = task.get("login_context", {}) or {}
    login = args.login if args.login is not None else login_context.get("login")
    password = (
        args.password
        if args.password is not None
        else login_context.get("password")
    )
    start_path = task.get("start_url", "/odoo")

    module = load_browser_use_module()
    namespace = argparse.Namespace(
        base_url=args.base_url,
        start_path=start_path,
        login=login,
        password=password,
        db=args.db,
        task=instruction,
    )
    prompt = module.build_task(namespace)
    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
