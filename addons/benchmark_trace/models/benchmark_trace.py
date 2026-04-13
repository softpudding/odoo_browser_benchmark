"""Benchmark trace recorder.

Captures all frontend→backend API calls during a benchmark episode.
State is stored in a module-level singleton so it persists across requests
within the same Odoo worker process.

Trace entries are stored in memory and retrieved via XML-RPC. For
multi-worker deployments, use ``--workers 0`` (single-process) or
write traces to a shared file/table.
"""

import json
import logging
import threading
import time
from typing import Any

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Module-level trace storage (shared across requests in one worker)
# ---------------------------------------------------------------------------

_trace_lock = threading.Lock()
_trace_active = False
_trace_session = ""
_trace_entries: list[dict] = []
_trace_counter = 0

# Methods that are reads (not writes)
_READ_METHODS = frozenset({
    "read", "search", "search_read", "search_count", "name_search",
    "name_get", "fields_get", "load_views", "onchange", "default_get",
    "read_group", "web_read_group", "web_search_read", "web_read",
    "get_views", "has_group", "read_progress_bar",
})


def is_active() -> bool:
    return _trace_active


def record_call(
    *,
    route: str,
    method: str = "",
    model: str = "",
    args_summary: str = "",
    uid: int | None = None,
    raised: bool = False,
    http_method: str = "",
) -> None:
    """Record a single API call. Thread-safe."""
    global _trace_counter
    if not _trace_active:
        return

    # Classify mutation: for ORM methods, use the known read/write sets.
    # For custom HTTP routes, use the HTTP method: GET = read, POST = write.
    if method and method in _READ_METHODS:
        mutation_class = "read"
    elif method:
        mutation_class = "write"
    elif http_method.upper() in ("GET", "HEAD", "OPTIONS"):
        mutation_class = "read"
    elif http_method.upper() == "POST":
        mutation_class = "write"
    else:
        mutation_class = "read"  # default unknown routes to read

    canonical = f"{model}.{method}" if model and method else f"custom:{route}"

    with _trace_lock:
        _trace_counter += 1
        _trace_entries.append({
            "seq": _trace_counter,
            "timestamp": time.time(),
            "route": route or "",
            "model": model or "",
            "method": method or "",
            "canonical_op": canonical,
            "mutation_class": mutation_class,
            "uid": uid or 0,
            "raised": raised,
            "args_summary": args_summary[:512] if args_summary else "",
        })


# ---------------------------------------------------------------------------
# Odoo model — provides XML-RPC interface
# ---------------------------------------------------------------------------

class BenchmarkTrace(models.TransientModel):
    _name = 'benchmark.trace'
    _description = 'Benchmark Trace Controller'

    @api.model
    def start_trace(self, session_name=""):
        """Start recording API calls. Clears any previous trace."""
        global _trace_active, _trace_session, _trace_entries, _trace_counter
        with _trace_lock:
            _trace_active = True
            _trace_session = session_name or f"trace_{int(time.time())}"
            _trace_entries = []
            _trace_counter = 0
        _logger.info("Benchmark trace started: %s", _trace_session)
        return {"session": _trace_session, "status": "recording"}

    @api.model
    def stop_trace(self):
        """Stop recording API calls."""
        global _trace_active
        _trace_active = False
        with _trace_lock:
            count = len(_trace_entries)
        _logger.info("Benchmark trace stopped: %s (%d entries)", _trace_session, count)
        return {"session": _trace_session, "entries": count, "status": "stopped"}

    @api.model
    def get_trace(self):
        """Return the full trace as a list of dicts."""
        with _trace_lock:
            return list(_trace_entries)

    @api.model
    def get_trace_summary(self):
        """Return a summary of the trace."""
        with _trace_lock:
            entries = list(_trace_entries)

        writes = [e for e in entries if e["mutation_class"] == "write"]
        reads = [e for e in entries if e["mutation_class"] == "read"]
        ops = {}
        for e in entries:
            ops[e["canonical_op"]] = ops.get(e["canonical_op"], 0) + 1

        return {
            "session": _trace_session,
            "total_calls": len(entries),
            "write_calls": len(writes),
            "read_calls": len(reads),
            "unique_ops": len(ops),
            "ops": ops,
            "write_ops": [e["canonical_op"] for e in writes],
        }

    @api.model
    def is_active(self):
        """Check if tracing is currently active."""
        return _trace_active
