"""Task scorer — computes the full metric vector for a completed run.

Reads the artifacts produced by ``run_task.py`` and applies the evaluation
logic from ``benchmark.metrics``.

Usage::

    scorer = TaskScorer(task, run_artifacts)
    result = scorer.score()
    scorer.write_report(output_dir)
"""

from __future__ import annotations

import json
import pathlib
from typing import Any

from benchmark.metrics import ScoreResult, compute_scores
from benchmark.schema import BenchmarkTask


class TaskScorer:
    """Scores a single benchmark run against its task oracles."""

    def __init__(self, task: BenchmarkTask, artifacts: dict[str, Any]) -> None:
        """
        Args:
            task: The benchmark task definition.
            artifacts: Dict with keys:
                - ``trace``: list of trace entry dicts
                - ``state_diff``: list of atomic edit dicts (observed)
                - ``expected_diff``: list of atomic edit dicts (from oracle)
                - ``wall_clock_sec``: float
                - ``browser_step_count``: int
                - ``token_cost``: float or None
                - ``violations``: list of violation dicts (from guard)
        """
        self.task = task
        self.artifacts = artifacts

    def score(self) -> ScoreResult:
        """Compute the full metric vector."""
        expected_dicts = self.artifacts.get("expected_diff", [])
        observed = _edits_from_dicts(self.artifacts.get("state_diff", []))

        trace = self.artifacts.get("trace", [])
        forbidden = self.task.forbidden_ops or self.task.trace_spec.forbidden_ops

        # Detect synthetic (count-only) oracles: they use sentinel keys
        # and norm_value=None, so exact-set comparison would always fail.
        # Instead, use count-aware matching.
        is_synthetic = any(
            isinstance(d.get("entity_key"), list)
            and len(d["entity_key"]) == 1
            and str(d["entity_key"][0]).startswith("__expected_")
            for d in expected_dicts
        )

        if is_synthetic:
            expected = _match_synthetic_oracle(expected_dicts, observed)
        else:
            expected = _edits_from_dicts(expected_dicts)

        result = compute_scores(
            expected_edits=expected,
            observed_edits=observed,
            trace_entries=trace,
            required_ops=self.task.trace_spec.required_ops,
            forbidden_ops=forbidden,
            wall_clock_sec=self.artifacts.get("wall_clock_sec", 0.0),
            browser_step_count=self.artifacts.get("browser_step_count", 0),
            token_cost=self.artifacts.get("token_cost"),
        )

        # Runs that exceeded budget (timeout or step limit) are failures
        # even if the final state happens to be correct.
        gave_up = self.artifacts.get("gave_up", False)
        if gave_up:
            result.outcome_success = False
            result.strict_success = False

        # Postcondition failures downgrade all primary metrics so that
        # rankings based on any primary metric reject the run.
        postcondition_failures = self.artifacts.get("postcondition_failures", [])
        if postcondition_failures:
            result.outcome_success = False
            result.strict_success = False
            result.state_diff_f1 = 0.0
            result.state_diff_precision = 0.0
            result.state_diff_recall = 0.0

        return result

    def write_report(self, output_dir: str | pathlib.Path) -> pathlib.Path:
        """Score and write all artifacts to disk.

        Produces:
        - ``score.json`` — the metric vector
        - ``trace.json`` — normalized trace
        - ``state_diff.json`` — observed DB diff
        - ``violations.json`` — contract violations (if any)

        Returns the path to ``score.json``.
        """
        output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        result = self.score()

        # Score JSON
        score_path = output_dir / "score.json"
        score_path.write_text(json.dumps(result.to_dict(), indent=2))

        # Trace JSON
        trace_path = output_dir / "trace.json"
        trace_path.write_text(json.dumps(
            self.artifacts.get("trace", []), indent=2,
        ))

        # State diff JSON
        diff_path = output_dir / "state_diff.json"
        diff_path.write_text(json.dumps(
            self.artifacts.get("state_diff", []), indent=2,
        ))

        # Expected diff JSON (oracle used during this run)
        expected_path = output_dir / "expected_state.json"
        expected_path.write_text(json.dumps(
            self.artifacts.get("expected_diff", []), indent=2,
        ))

        # Violations
        violations = self.artifacts.get("violations", [])
        if violations:
            viol_path = output_dir / "violations.json"
            viol_path.write_text(json.dumps(violations, indent=2))

        # Postcondition failures
        postcondition_failures = self.artifacts.get("postcondition_failures", [])
        pc_path = output_dir / "postcondition_failures.json"
        pc_path.write_text(json.dumps(postcondition_failures, indent=2))

        return score_path


def _edits_from_dicts(edit_dicts: list[dict]) -> set:
    """Reconstruct a set of AtomicEdit from serialized dicts."""
    from benchmark.instrumentation.state_snapshot import AtomicEdit

    edits = set()
    for d in edit_dicts:
        norm_value = d.get("norm_value")
        # Make norm_value hashable
        if isinstance(norm_value, list):
            norm_value = tuple(norm_value)
        elif isinstance(norm_value, dict):
            norm_value = tuple(sorted(norm_value.items()))

        entity_key = d.get("entity_key", ())
        if isinstance(entity_key, list):
            entity_key = tuple(entity_key)

        edits.add(AtomicEdit(
            model=d["model"],
            entity_key=entity_key,
            field=d["field"],
            op=d["op"],
            norm_value=norm_value,
        ))
    return edits


def _match_synthetic_oracle(expected_dicts: list[dict], observed: set) -> set:
    """Match a count-based synthetic oracle against observed edits.

    Synthetic oracles have sentinel entity_keys and ``norm_value=None``.
    Instead of exact-set comparison, we replace each sentinel with a
    matching observed edit (if one exists). Unmatched sentinels remain
    as-is so that ``state_diff_f1`` correctly penalizes missing edits.

    This means:
    - If the agent created the right records, all sentinels are replaced
      and ``expected == observed``, giving F1 = 1.0.
    - If the agent created too few records, unmatched sentinels remain,
      so recall drops.
    - If the agent created extra records, they appear only in observed,
      so precision drops.
    """
    from benchmark.instrumentation.state_snapshot import AtomicEdit
    from collections import defaultdict

    # Group observed by (model, field, op)
    observed_by_key: dict[tuple, list] = defaultdict(list)
    for edit in observed:
        key = (edit.model, edit.field, edit.op)
        observed_by_key[key].append(edit)

    # Track which observed edits have been claimed
    claimed: set[AtomicEdit] = set()
    result: set[AtomicEdit] = set()

    for d in expected_dicts:
        key = (d["model"], d["field"], d["op"])
        candidates = observed_by_key.get(key, [])

        # Find the first unclaimed candidate
        matched = None
        for c in candidates:
            if c not in claimed:
                matched = c
                break

        if matched is not None:
            # Replace sentinel with the real observed edit
            claimed.add(matched)
            result.add(matched)
        else:
            # No match found — keep the sentinel so recall is penalized
            entity_key = d.get("entity_key", ())
            if isinstance(entity_key, list):
                entity_key = tuple(entity_key)
            norm_value = d.get("norm_value")
            if isinstance(norm_value, list):
                norm_value = tuple(norm_value)
            result.add(AtomicEdit(
                model=d["model"],
                entity_key=entity_key,
                field=d["field"],
                op=d["op"],
                norm_value=norm_value,
            ))

    return result
