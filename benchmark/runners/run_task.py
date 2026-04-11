"""Task runner — orchestrates a single benchmark episode (Section 16).

Responsible for:
1. Loading the task definition
2. Restoring the database seed / running the setup script
3. Installing instrumentation (server tracer, client capture, state snapshot)
4. Launching the agent with the task instruction
5. Enforcing time/step limits and the agent contract
6. Collecting artifacts and invoking the scorer

Usage::

    runner = TaskRunner(task_dir="benchmark/tasks/website_hr_recruitment.apply_guru_job")
    result = runner.run(agent_fn=my_agent, odoo_env=env, page=playwright_page)
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import time
from typing import Any, Callable, Protocol

from benchmark.instrumentation.client_capture import ClientCapture
from benchmark.instrumentation.server_tracer import ServerTracer
from benchmark.instrumentation.state_snapshot import StateSnapshot
from benchmark.runners.runner_guard import RunnerGuard
from benchmark.runners.score_task import TaskScorer
from benchmark.schema import BenchmarkTask, load_task


class AgentFn(Protocol):
    """Protocol for the agent callable.

    The runner calls this with the task instruction, a Playwright page,
    and optional kwargs. The agent should perform browser actions and
    return when done (or when it gives up).

    Returns a dict with optional keys:
    - ``steps``: number of browser steps taken
    - ``token_cost``: LLM token cost if available
    - ``gave_up``: bool if the agent gave up
    """
    def __call__(
        self,
        instruction: str,
        page: Any,
        start_url: str,
        **kwargs: Any,
    ) -> dict[str, Any]: ...


class TaskRunner:
    """Runs a single benchmark task end-to-end."""

    def __init__(self, task_dir: str | pathlib.Path) -> None:
        self.task_dir = pathlib.Path(task_dir)
        self.task: BenchmarkTask = load_task(self.task_dir)
        self.tracer = ServerTracer()
        self.client_capture = ClientCapture()
        self.guard = RunnerGuard(
            agent_interface=self.task.agent_interface,
            task_dir=str(self.task_dir),
        )

    def run_setup(self, env: Any, *, restore_fn: Any | None = None) -> Any:
        """Restore the database seed and run the setup script.

        Args:
            env: Odoo ``Environment`` instance.
            restore_fn: Optional callable ``restore_fn(snapshot_name)``
                that restores the database to the named snapshot and
                **returns a fresh Environment** bound to the restored DB.
                When provided and ``db_seed.snapshot`` is declared, the
                runner calls it before executing the setup script.

        Returns:
            The (possibly new) Environment to use for the rest of the run.
            If ``restore_fn`` returns a new env, that is used; otherwise
            the original ``env`` is returned.
        """
        # Step 1: Restore DB snapshot if declared
        snapshot = self.task.db_seed.get("snapshot")
        if snapshot:
            if restore_fn is not None:
                new_env = restore_fn(snapshot)
                if new_env is not None:
                    env = new_env
            else:
                import warnings
                warnings.warn(
                    f"Task {self.task.task_id} declares db_seed.snapshot="
                    f"'{snapshot}' but no restore_fn was provided. "
                    f"Database state may not be clean.",
                    stacklevel=2,
                )

        # Step 2: Run setup script
        if not self.task.setup_script:
            return env

        setup_path = pathlib.Path(self.task.setup_script)
        if not setup_path.is_absolute():
            setup_path = self.task_dir / setup_path

        if not setup_path.exists():
            raise FileNotFoundError(f"Setup script not found: {setup_path}")

        spec = importlib.util.spec_from_file_location("benchmark_seed", setup_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load setup script: {setup_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if hasattr(mod, "setup"):
            mod.setup(env)

        # Commit seeded data so it's visible to the browser session,
        # which uses separate HTTP requests with their own cursors.
        if hasattr(env, "cr"):
            env.cr.commit()

        return env

    def run(
        self,
        agent_fn: Callable[..., dict[str, Any]],
        odoo_env: Any,
        page: Any,
        *,
        dataset_controller_cls: type | None = None,
        model_service_module: Any | None = None,
        base_model_cls: type | None = None,
        restore_fn: Any | None = None,
        output_dir: str | pathlib.Path | None = None,
    ) -> dict[str, Any]:
        """Execute a full benchmark episode.

        Args:
            agent_fn: The agent callable (see ``AgentFn`` protocol).
            odoo_env: An Odoo ``Environment`` instance for state snapshots.
            page: A Playwright ``Page`` for the browser session.
            dataset_controller_cls: The ``DataSet`` controller class for
                server-side tracing. If None, server tracing is skipped.
            model_service_module: ``odoo.service.model`` module. When
                provided, ``execute_cr`` is patched to capture all ORM
                dispatch including custom controller routes.
            base_model_cls: ``odoo.models.BaseModel`` class. When provided,
                ``create/write/unlink`` are patched to capture direct ORM
                writes from custom controllers (e.g. ``/website/form/*``).
            output_dir: Optional directory to write artifacts. If None,
                artifacts are returned but not persisted.

        Returns:
            Dict with keys: ``score``, ``trace``, ``state_diff``,
            ``violations``, ``agent_result``.
        """
        # 1. Restore DB seed and run setup (may return a fresh env)
        odoo_env = self.run_setup(odoo_env, restore_fn=restore_fn)

        # 2. Install instrumentation
        state_snap = StateSnapshot(odoo_env, self.task.state_spec)
        state_snap.capture_before()

        self.tracer.start()
        has_trace_reqs = bool(
            self.task.trace_spec.required_ops
            or self.task.trace_spec.forbidden_ops
        )
        if dataset_controller_cls is not None:
            self.tracer.install(
                dataset_controller_cls,
                model_service_module=model_service_module,
            )
        elif model_service_module is not None:
            self.tracer.install_execute_cr(model_service_module)
        elif has_trace_reqs:
            import warnings
            warnings.warn(
                f"Task {self.task.task_id} declares required/forbidden "
                f"trace ops but no server-side tracing hooks were provided "
                f"(dataset_controller_cls, model_service_module, or "
                f"base_model_cls). Trace-based metrics will be inaccurate.",
                stacklevel=2,
            )
        if base_model_cls is not None:
            self.tracer.install_orm_hooks(base_model_cls)
        elif self.task.trace_spec.required_ops:
            # Warn if required ops include custom routes but no ORM hooks
            has_custom = any(
                op.startswith("custom:") for op in self.task.trace_spec.required_ops
            )
            if has_custom:
                import warnings
                warnings.warn(
                    f"Task {self.task.task_id} requires custom-route trace "
                    f"ops but base_model_cls was not provided. ORM-level "
                    f"writes (e.g. /website/form/*) will not be traced. "
                    f"Pass base_model_cls=odoo.models.BaseModel to enable.",
                    stacklevel=2,
                )

        self.client_capture.install_sync(page)

        # Install guard on the Playwright page to enforce browser-only contract
        self.guard.start()
        self.guard.install_on_page(page)

        # Protect oracle files from agent reads by restricting permissions
        self._protect_oracle_files()

        # 3. Run the agent with enforced time limit
        t0 = time.time()
        timeout = self.task.time_limit_sec

        # Use a watchdog timer instead of running the agent on a
        # separate thread. Playwright's sync API has thread affinity
        # and must run on the thread that created the page.
        watchdog = _TimeoutWatchdog(timeout, page)
        watchdog.start()
        try:
            agent_result = agent_fn(
                instruction=self.task.instruction,
                page=page,
                start_url=self.task.start_url,
                time_limit_sec=timeout,
                step_limit=self.task.step_limit,
                login=self.task.login_context.login,
                password=self.task.login_context.password,
                groups=self.task.login_context.groups,
            )
        except Exception as exc:
            if watchdog.fired:
                agent_result = {"gave_up": True, "reason": "timeout"}
            else:
                agent_result = {"gave_up": True, "reason": str(exc)}

        finally:
            # Always clean up instrumentation, even on BaseException
            # (e.g. KeyboardInterrupt, SystemExit)
            watchdog.cancel()
            self._restore_oracle_files()
            self.tracer.stop()
            self.tracer.uninstall()
            self.guard.uninstall_from_page()
            self.guard.stop()

        wall_clock = time.time() - t0

        # Enforce total wall-clock limit: even if the agent returned
        # normally, mark it as timed out if it exceeded the limit
        if wall_clock > timeout and not agent_result.get("gave_up"):
            agent_result = {
                **agent_result,
                "gave_up": True,
                "reason": f"exceeded wall-clock limit ({wall_clock:.1f}s > {timeout}s)",
            }

        # Enforce step limit against measured browser interactions
        # (XHR/fetch/navigation only, not static asset loads)
        measured_steps = sum(
            1 for e in self.client_capture.get_entries()
            if e.get("resource_type") in ("xhr", "fetch", "document", None)
        )
        if (self.task.step_limit
                and measured_steps > self.task.step_limit
                and not agent_result.get("gave_up")):
            agent_result = {
                **agent_result,
                "gave_up": True,
                "reason": f"exceeded step limit ({measured_steps} > {self.task.step_limit})",
            }

        # 5. Capture after-state
        state_snap.capture_after()
        observed_diff = state_snap.get_diff_json()
        trace = self.tracer.get_trace()

        # 6. Build expected diff from state_spec (for scoring)
        expected_diff = self._build_expected_diff(odoo_env)

        # 6b. Run postcondition checks from check.py
        postcondition_failures = self._run_postconditions(odoo_env)

        # 7. Score
        artifacts = {
            "trace": trace,
            "state_diff": observed_diff,
            "expected_diff": expected_diff,
            "wall_clock_sec": wall_clock,
            # Measure browser steps from captured XHR/fetch/navigation
            # requests, excluding static asset loads (JS, CSS, images,
            # fonts) which inflate the count during normal page loads.
            "browser_step_count": sum(
                1 for e in self.client_capture.get_entries()
                if e.get("resource_type") in (
                    "xhr", "fetch", "document", None
                )
            ),
            "token_cost": agent_result.get("token_cost"),
            "gave_up": agent_result.get("gave_up", False),
            "violations": self.guard.get_violations(),
            "client_capture": self.client_capture.get_jsonrpc_entries(),
            "postcondition_failures": postcondition_failures,
        }

        scorer = TaskScorer(self.task, artifacts)
        score = scorer.score()

        # 8. Persist if output_dir specified
        if output_dir is not None:
            scorer.write_report(output_dir)
            # Also write client capture and agent result
            out = pathlib.Path(output_dir)
            (out / "client_capture.json").write_text(
                json.dumps(artifacts["client_capture"], indent=2)
            )
            (out / "agent_result.json").write_text(
                json.dumps(agent_result, indent=2, default=str)
            )

        return {
            "score": score.to_dict(),
            "trace": trace,
            "state_diff": observed_diff,
            "violations": self.guard.get_violations(),
            "agent_result": agent_result,
        }

    def _run_postconditions(self, odoo_env: Any) -> list[str]:
        """Run postcondition checks from ``check.py`` in the task directory.

        The check script should define a ``check(env) -> list[str]``
        function that returns a list of failure messages (empty = pass).
        This enables task-specific validation beyond state-diff matching,
        such as verifying chatter message content.
        """
        check_path = self.task_dir / "check.py"
        if not check_path.exists():
            return []

        try:
            spec = importlib.util.spec_from_file_location("benchmark_check", check_path)
            if spec is None or spec.loader is None:
                return []
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "check"):
                failures = mod.check(odoo_env)
                return failures if isinstance(failures, list) else []
        except Exception as exc:
            return [f"Postcondition check error: {exc}"]

        return []

    # -- Oracle file protection --------------------------------------------

    _ORACLE_FILES = ("task.yaml", "trace_spec.yaml", "state_spec.yaml",
                     "expected_state.json", "acl_spec.yaml", "metadata.json",
                     "check.py")

    def _protect_oracle_files(self) -> None:
        """Remove read permissions from oracle files during agent execution.

        This is a defense-in-depth measure: even if a Python-based agent
        tries to ``open()`` the oracle files, the OS will deny the read.
        Permissions are restored by ``_restore_oracle_files()``.
        """
        import stat
        self._saved_permissions: dict[pathlib.Path, int] = {}
        for name in self._ORACLE_FILES:
            path = self.task_dir / name
            if path.exists():
                mode = path.stat().st_mode
                self._saved_permissions[path] = mode
                # Remove all read permissions
                path.chmod(mode & ~(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH))

    def _restore_oracle_files(self) -> None:
        """Restore original permissions on oracle files."""
        for path, mode in getattr(self, "_saved_permissions", {}).items():
            try:
                path.chmod(mode)
            except OSError:
                pass

    def _build_expected_diff(self, odoo_env: Any | None = None) -> list[dict]:
        """Build the expected atomic edits from the task's state_spec.

        Resolution order:
        1. ``expected_state.json`` in the task directory (explicit oracle).
        2. ``seed.py:get_expected_state(env)`` if the function exists.
        3. Synthetic oracle derived from ``state_spec.expected_changes``.
        """
        # 1. Explicit oracle file
        expected_path = self.task_dir / "expected_state.json"
        if expected_path.exists():
            return json.loads(expected_path.read_text())

        # 2. Programmatic oracle from the seed module
        seed_path = self.task_dir / "seed.py"
        if seed_path.exists() and odoo_env is not None:
            spec = importlib.util.spec_from_file_location("benchmark_seed", seed_path)
            if spec is not None and spec.loader is not None:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "get_expected_state"):
                    return mod.get_expected_state(odoo_env)

        # 3. Synthetic oracle from state_spec expected_changes
        # When only expected_changes counts are available, we build
        # placeholder edits that StateSnapshot.compute_diff() will
        # compare against the actual observed diff. This ensures
        # outcome_success is based on the observed diff matching the
        # declared change counts rather than being vacuously true/false.
        return self._synthetic_expected_diff()

    def _synthetic_expected_diff(self) -> list[dict]:
        """Build a count-based synthetic oracle from state_spec.

        Returns ``_SENTINEL_EXPECTED`` which signals the scorer to use
        count-based comparison instead of exact edit matching.
        """
        edits: list[dict] = []
        for model_name, model_spec in self.task.state_spec.models.items():
            if model_spec.optional:
                continue
            for op, count in model_spec.expected_changes.items():
                for i in range(count):
                    # One sentinel edit per expected change, per tracked field.
                    # These use a synthetic entity_key that will be matched
                    # against observed edits by the scorer's count-aware path.
                    for field_name in model_spec.fields:
                        if field_name in set(model_spec.ignore_fields):
                            continue
                        edits.append({
                            "model": model_name,
                            "entity_key": [f"__expected_{i}__"],
                            "field": field_name,
                            "op": op,
                            "norm_value": None,  # any value accepted
                        })
        return edits


class _TimeoutWatchdog:
    """Watchdog timer for enforcing benchmark time limits.

    Enforcement is two-layered:

    1. **Playwright per-op timeout**: ``start()`` sets
       ``page.set_default_timeout()`` so individual browser operations
       fail after the deadline. This interrupts agents stuck in a single
       long Playwright call.
    2. **Post-run wall-clock check**: ``TaskRunner.run()`` checks total
       elapsed time after the agent returns and marks the run as
       timed out if it exceeded the limit. This catches agents that
       spend time in non-Playwright work (LLM planning, sleep, etc.).

    The watchdog does NOT call ``page.close()`` from a background thread
    because Playwright's sync API is thread-affine.
    """

    def __init__(self, timeout_sec: int, page: Any) -> None:
        self.timeout_sec = timeout_sec
        self.page = page
        self.fired = False
        self.deadline = time.time() + timeout_sec

    def start(self) -> None:
        """Configure Playwright's default timeout to the remaining time."""
        try:
            if self.page is not None:
                # Set Playwright's default timeout (in ms) so any
                # operation that exceeds the deadline raises TimeoutError
                self.page.set_default_timeout(self.timeout_sec * 1000)
        except Exception:
            pass

    def cancel(self) -> None:
        """Mark the watchdog as complete (agent finished in time)."""
        self.fired = False
