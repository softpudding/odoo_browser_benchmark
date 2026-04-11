"""Evaluation metrics — Section 11 of the spec.

Computes the benchmark metric vector:
  - OutcomeSuccess, StrictSuccess, StateDiffF1 (primary)
  - RequiredOpRecall, WritePrecision, HarmfulWriteRate (trace)
  - Efficiency metrics (wall clock, steps, calls, tokens)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------------------
# StateDiffF1 (Section 9.5)
# ---------------------------------------------------------------------------

def state_diff_f1(
    expected: set,
    observed: set,
    weights: dict | None = None,
) -> dict[str, float]:
    """Compute precision, recall, and F1 over atomic-edit sets.

    Both *expected* (G) and *observed* (P) are sets of ``AtomicEdit``.
    By default every edit has unit weight.

    Returns dict with keys ``precision``, ``recall``, ``f1``.
    """
    if not expected and not observed:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}

    w = weights or {}

    def weight(a: Any) -> float:
        return w.get(a, 1.0)

    intersection = expected & observed
    sum_intersection = sum(weight(a) for a in intersection)
    sum_observed = sum(weight(a) for a in observed)
    sum_expected = sum(weight(a) for a in expected)

    precision = sum_intersection / sum_observed if sum_observed > 0 else 0.0
    recall = sum_intersection / sum_expected if sum_expected > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {"precision": precision, "recall": recall, "f1": f1}


# ---------------------------------------------------------------------------
# Outcome metrics (Section 11.1)
# ---------------------------------------------------------------------------

def outcome_success(expected: set, observed: set) -> bool:
    """Binary exact success: observed state delta matches expected exactly."""
    return expected == observed


def strict_success(
    expected: set,
    observed: set,
    trace_entries: list[dict],
    forbidden_ops: list[str],
) -> bool:
    """OutcomeSuccess AND no forbidden operation was fired."""
    if not outcome_success(expected, observed):
        return False
    fired_ops = {e["canonical_op"] for e in trace_entries}
    return not any(op in fired_ops for op in forbidden_ops)


# ---------------------------------------------------------------------------
# Trace metrics (Section 11.2)
# ---------------------------------------------------------------------------

def required_op_recall(
    required_ops: list[str],
    trace_entries: list[dict],
) -> float:
    """Set recall over required operations."""
    if not required_ops:
        return 1.0
    fired = {e["canonical_op"] for e in trace_entries}
    hits = sum(1 for op in required_ops if op in fired)
    return hits / len(required_ops)


def write_precision(
    trace_entries: list[dict],
    forbidden_ops: list[str],
) -> float:
    """Fraction of observed write events that are not forbidden."""
    writes = [e for e in trace_entries if e.get("mutation_class") == "write"]
    if not writes:
        return 1.0
    forbidden_set = set(forbidden_ops)
    good = sum(1 for e in writes if e["canonical_op"] not in forbidden_set)
    return good / len(writes)


def harmful_write_rate(
    trace_entries: list[dict],
    forbidden_ops: list[str],
) -> float:
    """Forbidden write events / max(1, total write events)."""
    writes = [e for e in trace_entries if e.get("mutation_class") == "write"]
    total = max(1, len(writes))
    forbidden_set = set(forbidden_ops)
    harmful = sum(1 for e in writes if e["canonical_op"] in forbidden_set)
    return harmful / total


def over_query_ratio(
    trace_entries: list[dict],
    required_ops: list[str],
) -> float:
    """Diagnostic: ratio of total reads to required ops.

    Higher values indicate excessive exploration / over-querying.
    """
    reads = sum(1 for e in trace_entries if e.get("mutation_class") == "read")
    baseline = max(1, len(required_ops))
    return reads / baseline


# ---------------------------------------------------------------------------
# Full scoring
# ---------------------------------------------------------------------------

@dataclass
class ScoreResult:
    """Complete metric vector for a benchmark run."""
    # Primary (Section 11.1)
    outcome_success: bool
    strict_success: bool
    state_diff_f1: float
    state_diff_precision: float
    state_diff_recall: float

    # Trace (Section 11.2)
    required_op_recall: float
    write_precision: float
    harmful_write_rate: float
    over_query_ratio: float

    # Efficiency (Section 11.3)
    wall_clock_sec: float
    browser_step_count: int
    backend_call_count: int
    write_call_count: int
    token_cost: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "outcome_success": self.outcome_success,
            "strict_success": self.strict_success,
            "state_diff_f1": self.state_diff_f1,
            "state_diff_precision": self.state_diff_precision,
            "state_diff_recall": self.state_diff_recall,
            "required_op_recall": self.required_op_recall,
            "write_precision": self.write_precision,
            "harmful_write_rate": self.harmful_write_rate,
            "over_query_ratio": self.over_query_ratio,
            "wall_clock_sec": self.wall_clock_sec,
            "browser_step_count": self.browser_step_count,
            "backend_call_count": self.backend_call_count,
            "write_call_count": self.write_call_count,
            "token_cost": self.token_cost,
        }


def compute_scores(
    *,
    expected_edits: set,
    observed_edits: set,
    trace_entries: list[dict],
    required_ops: list[str],
    forbidden_ops: list[str],
    wall_clock_sec: float = 0.0,
    browser_step_count: int = 0,
    token_cost: float | None = None,
    weights: dict | None = None,
) -> ScoreResult:
    """Compute the full metric vector for a single task run."""
    f1_result = state_diff_f1(expected_edits, observed_edits, weights)

    writes = [e for e in trace_entries if e.get("mutation_class") == "write"]

    return ScoreResult(
        outcome_success=outcome_success(expected_edits, observed_edits),
        strict_success=strict_success(expected_edits, observed_edits, trace_entries, forbidden_ops),
        state_diff_f1=f1_result["f1"],
        state_diff_precision=f1_result["precision"],
        state_diff_recall=f1_result["recall"],
        required_op_recall=required_op_recall(required_ops, trace_entries),
        write_precision=write_precision(trace_entries, forbidden_ops),
        harmful_write_rate=harmful_write_rate(trace_entries, forbidden_ops),
        over_query_ratio=over_query_ratio(trace_entries, required_ops),
        wall_clock_sec=wall_clock_sec,
        browser_step_count=browser_step_count,
        backend_call_count=len(trace_entries),
        write_call_count=len(writes),
        token_cost=token_cost,
    )
