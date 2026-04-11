"""Database state snapshot and diff — Sections 9 and 5.5 of the spec.

Captures normalized, model-scoped database state before and after an
agent episode, then computes the atomic-edit diff used by ``StateDiffF1``.

Usage::

    snap = StateSnapshot(env, state_spec)
    snap.capture_before()
    # ... run agent episode ...
    snap.capture_after()
    diff = snap.compute_diff()
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# These are always ignored unless the task explicitly includes them.
DEFAULT_IGNORE_FIELDS = frozenset({
    "id", "create_date", "write_date", "__last_update",
    "create_uid", "write_uid",
})

# Models that generate noise unrelated to task intent.
DEFAULT_IGNORE_MODELS = frozenset({
    "bus.bus", "bus.presence",
    "ir.logging",
    "base.registry.signaling",
    "ir.attachment",  # cache entries, unless task-relevant
})


# ---------------------------------------------------------------------------
# Atomic edit (Section 9.5)
# ---------------------------------------------------------------------------

@dataclass(frozen=True, eq=True)
class AtomicEdit:
    """One unit of state change: ``(model, entity_key, field, op, norm_value)``."""
    model: str
    entity_key: tuple  # business-key values, hashable
    field: str
    op: str  # "create" | "delete" | "set"
    norm_value: Any = None

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "entity_key": list(self.entity_key),
            "field": self.field,
            "op": self.op,
            "norm_value": _json_safe(self.norm_value),
        }


def _json_safe(v: Any) -> Any:
    """Make a value JSON-serializable."""
    if isinstance(v, (str, int, float, bool, type(None))):
        return v
    if isinstance(v, (list, tuple)):
        return [_json_safe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _json_safe(val) for k, val in v.items()}
    return str(v)


def _normalize_value(val: Any) -> Any:
    """Normalize an ORM field value for comparison."""
    # Check for Odoo recordset first (x2many and m2o) — recordsets have
    # `ids` but are NOT plain list/tuple, so this must come before the
    # isinstance check.
    if hasattr(val, "ids"):
        ids = val.ids
        if len(ids) <= 1 and hasattr(val, "display_name"):
            # Many2one (single record) — use display_name for portability
            if not ids:
                return None
            return str(val.display_name or val.id)
        # One2many / Many2many — sorted tuple of display names
        return tuple(sorted(
            str(getattr(r, "display_name", None) or r.id)
            for r in val
        ))
    if isinstance(val, (list, tuple)):
        return tuple(sorted(val))
    if hasattr(val, "id"):
        name = getattr(val, "display_name", None) or getattr(val, "name", str(val.id))
        return str(name)
    if isinstance(val, bytes):
        return val.hex()[:32]
    return val


def _extract_entity_key(record: Any, match_key_fields: list[str]) -> tuple:
    """Build the entity key for a record from the match_key fields.

    Relational fields (Many2one) are normalized to their ``display_name``
    rather than their database ID, so entity keys remain portable across
    runs with different primary key sequences.
    """
    parts = []
    for f in match_key_fields:
        val = getattr(record, f, None)
        if hasattr(val, "id") and hasattr(val, "display_name"):
            # Many2one recordset — use display_name for portability
            val = val.display_name or str(val.id)
        parts.append(val)
    return tuple(parts)


# ---------------------------------------------------------------------------
# State snapshot
# ---------------------------------------------------------------------------

class StateSnapshot:
    """Captures and diffs database state around a benchmark episode."""

    def __init__(self, env: Any, state_spec: Any) -> None:
        """
        Args:
            env: An Odoo ``Environment`` instance.
            state_spec: A ``StateSpec`` from ``benchmark.schema``.
        """
        self.env = env
        self.state_spec = state_spec
        self._before: dict[str, dict[tuple, dict[str, Any]]] = {}
        self._after: dict[str, dict[tuple, dict[str, Any]]] = {}

    def _read_model(self, model_name: str) -> dict[tuple, dict[str, Any]]:
        """Read all records for a model, keyed by entity key."""
        from benchmark.schema import ModelStateSpec
        spec: ModelStateSpec = self.state_spec.models.get(model_name)
        if spec is None:
            return {}

        Model = self.env[model_name]
        records = Model.search([])

        # Default ignore fields are only applied for fields NOT explicitly
        # listed in the task's state_spec. If a task intentionally tracks
        # id, timestamps, or audit fields, they are honored.
        explicit_fields = set(spec.fields)
        ignore = set(spec.ignore_fields) | (DEFAULT_IGNORE_FIELDS - explicit_fields)
        read_fields = [f for f in spec.fields if f not in ignore]
        match_key = spec.match_key or ["id"]

        result: dict[tuple, dict[str, Any]] = {}
        key_counts: dict[tuple, int] = {}
        for rec in records:
            base_key = _extract_entity_key(rec, match_key)
            # Disambiguate duplicate business keys by appending a counter
            count = key_counts.get(base_key, 0)
            key_counts[base_key] = count + 1
            key = base_key if count == 0 else (*base_key, f"#dup{count}")
            vals = {}
            for f in read_fields:
                val = getattr(rec, f, None)
                vals[f] = _normalize_value(val)
            result[key] = vals
        return result

    def capture_before(self) -> None:
        """Snapshot the state of all models in the state spec."""
        for model_name in self.state_spec.models:
            # Models in DEFAULT_IGNORE_MODELS are skipped UNLESS the task
            # explicitly includes them in state_spec (e.g. ir.attachment
            # for upload benchmarks).
            # Since we're iterating self.state_spec.models, these are all
            # explicitly declared, so we never skip them here.
            self._before[model_name] = self._read_model(model_name)

    def capture_after(self) -> None:
        """Snapshot the state of all models after the episode.

        Invalidates the ORM cache first to ensure we read the actual
        committed state from the database, not stale cached values
        from ``capture_before()``.
        """
        # Invalidate ORM cache so we see the agent's committed changes
        if hasattr(self.env, "invalidate_all"):
            self.env.invalidate_all()
        # Use a fresh cursor to ensure we read committed data
        if hasattr(self.env, "cr") and hasattr(self.env.cr, "commit"):
            try:
                self.env.cr.commit()
            except Exception:
                pass

        for model_name in self.state_spec.models:
            # Models in DEFAULT_IGNORE_MODELS are skipped UNLESS the task
            # explicitly includes them in state_spec (e.g. ir.attachment
            # for upload benchmarks).
            # Since we're iterating self.state_spec.models, these are all
            # explicitly declared, so we never skip them here.
            self._after[model_name] = self._read_model(model_name)

    def compute_diff(self, *, include_optional: bool = True) -> set[AtomicEdit]:
        """Compute the set of atomic edits between before and after states.

        Args:
            include_optional: If False, models marked ``optional: true``
                in the state spec are excluded from the diff. Use False
                for outcome scoring so optional side-effects don't affect
                precision/recall.
        """
        edits: set[AtomicEdit] = set()

        for model_name in self.state_spec.models:
            # Models in DEFAULT_IGNORE_MODELS are skipped UNLESS the task
            # explicitly includes them in state_spec (e.g. ir.attachment
            # for upload benchmarks).
            # Since we're iterating self.state_spec.models, these are all
            # explicitly declared, so we never skip them here.
            spec = self.state_spec.models[model_name]
            if not include_optional and spec.optional:
                continue

            before = self._before.get(model_name, {})
            after = self._after.get(model_name, {})

            explicit_fields = set(spec.fields)
            ignore = set(spec.ignore_fields) | (DEFAULT_IGNORE_FIELDS - explicit_fields)
            check_fields = [f for f in spec.fields if f not in ignore]

            # New records (created)
            for key in after:
                if key not in before:
                    for f in check_fields:
                        val = after[key].get(f)
                        edits.add(AtomicEdit(
                            model=model_name,
                            entity_key=key,
                            field=f,
                            op="create",
                            norm_value=val,
                        ))

            # Deleted records
            for key in before:
                if key not in after:
                    for f in check_fields:
                        val = before[key].get(f)
                        edits.add(AtomicEdit(
                            model=model_name,
                            entity_key=key,
                            field=f,
                            op="delete",
                            norm_value=val,
                        ))

            # Modified records
            for key in after:
                if key in before:
                    for f in check_fields:
                        old_val = before[key].get(f)
                        new_val = after[key].get(f)
                        if old_val != new_val:
                            edits.add(AtomicEdit(
                                model=model_name,
                                entity_key=key,
                                field=f,
                                op="set",
                                norm_value=new_val,
                            ))

        return edits

    def get_before_state(self) -> dict[str, Any]:
        """Return serialized before-state."""
        return {
            model: {str(k): v for k, v in records.items()}
            for model, records in self._before.items()
        }

    def get_after_state(self) -> dict[str, Any]:
        """Return serialized after-state."""
        return {
            model: {str(k): v for k, v in records.items()}
            for model, records in self._after.items()
        }

    def get_diff_json(self, *, include_optional: bool = False) -> list[dict]:
        """Return the diff as a JSON-serializable list of atomic edits.

        By default, optional models are excluded so the diff is suitable
        for outcome scoring. Pass ``include_optional=True`` for diagnostic
        purposes.
        """
        return [e.to_dict() for e in sorted(
            self.compute_diff(include_optional=include_optional),
            key=lambda e: (e.model, e.entity_key, e.field),
        )]
