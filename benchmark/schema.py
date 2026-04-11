"""Benchmark object model — Section 7 of the spec.

Each benchmark task is a tuple:
  T = (instruction, db_seed, user_context, start_url, trace_oracle,
       state_oracle, agent_contract, constraints)

This module defines the dataclass representations and YAML loading helpers.
"""

from __future__ import annotations

import pathlib
from dataclasses import dataclass, field
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Trace spec (Section 10)
# ---------------------------------------------------------------------------

@dataclass
class TraceSpec:
    """Which backend operations are required / optional / forbidden."""
    required_ops: list[str] = field(default_factory=list)
    optional_ops: list[str] = field(default_factory=list)
    forbidden_ops: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# State spec (Section 9)
# ---------------------------------------------------------------------------

_DEFAULT_IGNORE_FIELDS = ["id", "create_date", "write_date", "__last_update"]


@dataclass
class ModelStateSpec:
    """Per-model expected state delta."""
    match_key: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list)
    ignore_fields: list[str] = field(default_factory=lambda: list(_DEFAULT_IGNORE_FIELDS))
    expected_changes: dict[str, int] = field(default_factory=dict)
    optional: bool = False
    weights: dict[str, float] = field(default_factory=dict)


@dataclass
class StateSpec:
    """Task-level state oracle."""
    models: dict[str, ModelStateSpec] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Login / ACL context
# ---------------------------------------------------------------------------

@dataclass
class LoginContext:
    login: str | None = "admin"  # None means public/anonymous access
    password: str | None = None
    groups: list[str] = field(default_factory=list)


@dataclass
class ACLSpec:
    login: str = ""
    denied_models: list[str] = field(default_factory=list)
    denied_ops: list[str] = field(default_factory=list)


@dataclass
class SafetyPolicy:
    no_writes_allowed: bool = False
    allowed_write_models: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Main task definition (Section 7.1)
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkTask:
    task_id: str
    module: str
    difficulty: str  # easy | medium | hard
    instruction: str
    start_url: str
    login_context: LoginContext
    agent_interface: str = "browser_only"

    # Database seed
    db_seed: dict[str, Any] = field(default_factory=dict)
    setup_script: str | None = None
    cleanup_script_optional: str | None = None

    # Limits
    time_limit_sec: int = 300
    step_limit: int = 100

    # Oracles
    trace_spec: TraceSpec = field(default_factory=TraceSpec)
    state_spec: StateSpec = field(default_factory=StateSpec)
    forbidden_ops: list[str] = field(default_factory=list)

    # Safety (optional)
    acl_spec: ACLSpec | None = None
    safety_policy: SafetyPolicy | None = None
    expected_denial_signal: dict[str, str] | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _load_yaml(path: pathlib.Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _build_login_context(raw: dict | str | None) -> LoginContext:
    if raw is None:
        return LoginContext()
    if isinstance(raw, str):
        return LoginContext(login=raw)
    # Preserve login=None (public/anonymous); only drop keys not in LoginContext
    valid_keys = {"login", "password", "groups"}
    return LoginContext(**{k: v for k, v in raw.items() if k in valid_keys})


def _build_trace_spec(raw: dict | None) -> TraceSpec:
    if not raw:
        return TraceSpec()
    return TraceSpec(
        required_ops=raw.get("required_ops", []),
        optional_ops=raw.get("optional_ops", []),
        forbidden_ops=raw.get("forbidden_ops", []),
    )


def _build_model_state_spec(raw: dict) -> ModelStateSpec:
    return ModelStateSpec(
        match_key=raw.get("match_key", []),
        fields=raw.get("fields", []),
        ignore_fields=raw.get("ignore_fields", list(_DEFAULT_IGNORE_FIELDS)),
        expected_changes=raw.get("expected_changes", {}),
        optional=raw.get("optional", False),
        weights=raw.get("weights", {}),
    )


def _build_state_spec(raw: dict | None) -> StateSpec:
    if not raw:
        return StateSpec()
    models = {}
    for model_name, model_raw in raw.get("models", {}).items():
        models[model_name] = _build_model_state_spec(model_raw)
    return StateSpec(models=models)


def load_task(task_dir: str | pathlib.Path) -> BenchmarkTask:
    """Load a benchmark task from its directory.

    Expects at minimum ``task.yaml``.  Optionally reads ``trace_spec.yaml``
    and ``state_spec.yaml`` as overrides / supplements.
    """
    task_dir = pathlib.Path(task_dir)
    raw = _load_yaml(task_dir / "task.yaml")

    # Load trace and state specs from dedicated files if present,
    # falling back to inline definitions in task.yaml.
    trace_file = task_dir / "trace_spec.yaml"
    trace_raw = _load_yaml(trace_file) if trace_file.exists() else raw.get("trace_spec")

    state_file = task_dir / "state_spec.yaml"
    state_raw = _load_yaml(state_file) if state_file.exists() else raw.get("state_spec")

    forbidden = raw.get("forbidden_ops", [])
    if trace_raw and not forbidden:
        forbidden = trace_raw.get("forbidden_ops", [])

    # ACL / safety (Section 13) — load from dedicated file or inline
    acl_file = task_dir / "acl_spec.yaml"
    acl_raw = _load_yaml(acl_file) if acl_file.exists() else (raw.get("acl_spec") or raw.get("acl_setup"))
    acl = ACLSpec(**acl_raw) if acl_raw else None

    safety_raw = raw.get("safety_policy")
    safety = None
    if safety_raw:
        safety = SafetyPolicy(**safety_raw)

    # Prompt override from prompt.md
    instruction = raw.get("instruction", "")
    prompt_file = task_dir / "prompt.md"
    if prompt_file.exists():
        instruction = prompt_file.read_text().strip()

    # Setup script path
    setup_script = raw.get("setup_script")
    if setup_script and not pathlib.Path(setup_script).is_absolute():
        seed_file = task_dir / setup_script
        if seed_file.exists():
            setup_script = str(seed_file)

    return BenchmarkTask(
        task_id=raw["task_id"],
        module=raw.get("module", ""),
        difficulty=raw.get("difficulty", "medium"),
        instruction=instruction,
        start_url=raw.get("start_url", "/"),
        login_context=_build_login_context(raw.get("login_context")),
        agent_interface=raw.get("agent_interface", "browser_only"),
        db_seed=raw.get("db_seed", {}),
        setup_script=setup_script,
        cleanup_script_optional=raw.get("cleanup_script_optional"),
        time_limit_sec=raw.get("time_limit_sec", 300),
        step_limit=raw.get("step_limit", 100),
        trace_spec=_build_trace_spec(trace_raw),
        state_spec=_build_state_spec(state_raw),
        forbidden_ops=forbidden,
        acl_spec=acl,
        safety_policy=safety,
        expected_denial_signal=raw.get("expected_denial_signal"),
        metadata=raw.get("metadata", {}),
    )


def task_to_dict(task: BenchmarkTask) -> dict:
    """Serialize a BenchmarkTask to a JSON-safe dict."""
    from dataclasses import asdict
    return asdict(task)
