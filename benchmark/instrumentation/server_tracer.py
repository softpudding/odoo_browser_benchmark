"""Server-side semantic capture — Section 8.2 of the spec.

Hooks into Odoo's JSON-RPC dispatch to capture every backend operation
with its canonical semantic form (e.g. ``sale.order.create``).

Usage::

    tracer = ServerTracer()
    tracer.install(registry)   # monkey-patches dispatch
    # ... run agent episode ...
    tracer.uninstall()
    trace = tracer.get_trace()
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Canonical operation mapping (Section 8.3)
# ---------------------------------------------------------------------------

_READ_METHODS = frozenset({
    "read", "search", "search_read", "search_count", "name_search",
    "name_get", "fields_get", "load_views", "onchange", "default_get",
    "read_group", "web_read_group", "web_search_read", "web_read",
    "get_views", "has_group",
})

_WRITE_METHODS = frozenset({
    "create", "write", "unlink", "copy",
    "action_confirm", "action_post", "action_cancel", "action_done",
    "action_draft", "action_lock", "action_unlock", "action_send",
    "action_set_draft", "action_validate", "action_assign",
    "button_confirm", "button_validate", "button_cancel", "button_draft",
    "button_done", "button_approve", "button_refuse",
    "message_post", "message_subscribe",
})


def classify_op(method: str) -> str:
    """Return ``'read'`` or ``'write'`` for a given ORM method name."""
    if method in _READ_METHODS:
        return "read"
    if method in _WRITE_METHODS:
        return "write"
    # Heuristic: action_* and button_* are writes
    if method.startswith(("action_", "button_")):
        return "write"
    # Default unknown methods to write (conservative)
    return "write"


def canonical_op(route: str, model: str | None, method: str | None) -> str:
    """Build the canonical semantic operation string.

    Returns e.g. ``"sale.order.create"`` for dataset/RPC calls,
    ``"custom:/website/form/hr.applicant"`` for custom HTTP routes, or
    both forms when an ORM write is triggered by a custom controller.

    When the route starts with ``custom:`` it is preserved as-is,
    since the caller explicitly tagged it as a custom controller route.
    For ORM-level hooks (``orm:`` or ``orm_direct`` routes), the
    ``model.method`` form is used.
    """
    if route.startswith("custom:"):
        return route
    if model and method:
        return f"{model}.{method}"
    return f"custom:{route}"


def diagnostic_tag(method: str | None, route: str | None) -> str | None:
    """Return an optional diagnostic tag (Section 8.4)."""
    if method in ("load_views", "get_views", "fields_get"):
        return "view_load"
    if method in ("read", "search_read", "web_search_read", "web_read"):
        return "decision_read"
    if route and "/web/session" in route:
        return "bootstrap"
    return None


# ---------------------------------------------------------------------------
# Trace entry
# ---------------------------------------------------------------------------

@dataclass
class TraceEntry:
    """A single captured backend operation."""
    request_id: int
    timestamp: float
    uid: int | None
    db: str | None
    route: str
    controller_type: str  # "jsonrpc" | "http" | "unknown"
    canonical_op: str
    model: str | None
    method: str | None
    args_summary: str  # truncated repr of args
    mutation_class: str  # "read" | "write"
    raised: bool = False
    committed: bool = True
    diagnostic_tag: str | None = None
    touched_models: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "uid": self.uid,
            "db": self.db,
            "route": self.route,
            "controller_type": self.controller_type,
            "canonical_op": self.canonical_op,
            "model": self.model,
            "method": self.method,
            "args_summary": self.args_summary,
            "mutation_class": self.mutation_class,
            "raised": self.raised,
            "committed": self.committed,
            "diagnostic_tag": self.diagnostic_tag,
            "touched_models": self.touched_models,
        }


# ---------------------------------------------------------------------------
# Server tracer
# ---------------------------------------------------------------------------

class ServerTracer:
    """Captures server-side semantic operations during a benchmark episode.

    Designed to be installed as a middleware / monkey-patch on Odoo's
    ``/web/dataset/call_kw`` and ``/web/dataset/call_button`` routes,
    as well as any ``type='jsonrpc'`` controller.
    """

    def __init__(self) -> None:
        self._entries: list[TraceEntry] = []
        self._lock = threading.Lock()
        self._counter = 0
        self._active = False
        self._originals: dict[str, Any] = {}

    # -- public API --------------------------------------------------------

    def start(self) -> None:
        """Begin capturing."""
        with self._lock:
            self._entries.clear()
            self._counter = 0
            self._active = True

    def stop(self) -> None:
        """Stop capturing."""
        self._active = False

    def record(
        self,
        *,
        route: str,
        controller_type: str = "jsonrpc",
        model: str | None = None,
        method: str | None = None,
        args: Any = None,
        uid: int | None = None,
        db: str | None = None,
        raised: bool = False,
        committed: bool = True,
    ) -> TraceEntry | None:
        """Record a single operation. Called from the patched dispatch."""
        if not self._active:
            return None

        with self._lock:
            self._counter += 1
            req_id = self._counter

        # Summarize args (truncated for storage)
        if args is not None:
            summary = repr(args)
            if len(summary) > 512:
                summary = summary[:509] + "..."
        else:
            summary = ""

        entry = TraceEntry(
            request_id=req_id,
            timestamp=time.time(),
            uid=uid,
            db=db,
            route=route,
            controller_type=controller_type,
            canonical_op=canonical_op(route, model, method),
            model=model,
            method=method,
            args_summary=summary,
            mutation_class=classify_op(method) if method else "write",
            raised=raised,
            committed=committed,
            diagnostic_tag=diagnostic_tag(method, route),
        )

        with self._lock:
            self._entries.append(entry)
        return entry

    def get_trace(self) -> list[dict[str, Any]]:
        """Return the full trace as a list of dicts."""
        with self._lock:
            return [e.to_dict() for e in self._entries]

    def get_entries(self) -> list[TraceEntry]:
        """Return raw TraceEntry objects."""
        with self._lock:
            return list(self._entries)

    # -- Odoo integration --------------------------------------------------

    def install(
        self,
        dataset_controller_cls: type,
        model_service_module: Any | None = None,
    ) -> None:
        """Monkey-patch Odoo dispatch to capture all backend operations.

        **Important**: For DataSet controller patches to take effect on
        live traffic, this must be called before Odoo builds its routing
        map (i.e., before ``http.root`` is initialized), OR the caller
        must also patch the bound endpoint in the routing rules. When
        called after startup, use ``install_orm_hooks()`` and/or
        ``install_execute_cr()`` which patch at the function/class level
        and always take effect regardless of routing map state.

        Patches two layers:

        1. ``DataSet.call_kw`` / ``call_button`` — captures explicit
           ``/web/dataset/*`` calls with full model/method/args context.
        2. ``odoo.service.model.execute_cr`` — captures **all** ORM calls
           dispatched through the RPC layer, including custom controller
           routes like ``/website/form/hr.applicant`` that bypass the
           DataSet controller entirely.

        Call ``uninstall()`` to restore the original functions.

        Args:
            dataset_controller_cls: The ``DataSet`` controller class from
                ``addons/web/controllers/dataset.py``.
            model_service_module: The ``odoo.service.model`` module.
                If provided, ``execute_cr`` is patched to capture all
                ORM dispatch including custom jsonrpc routes.
        """
        tracer = self

        # -- Layer 1: DataSet controller patches ---------------------------

        original_call_kw = dataset_controller_cls.call_kw
        original_call_button = dataset_controller_cls.call_button

        def traced_call_kw(self_ctrl, model, method, args, kwargs, path=None):
            uid = getattr(getattr(self_ctrl, "env", None), "uid", None)
            db = getattr(getattr(self_ctrl, "env", None), "cr", None)
            db = getattr(db, "dbname", None) if db else None
            raised = False
            try:
                result = original_call_kw(self_ctrl, model, method, args, kwargs, path=path)
            except Exception:
                raised = True
                raise
            finally:
                tracer.record(
                    route="/web/dataset/call_kw",
                    model=model,
                    method=method,
                    args=args,
                    uid=uid,
                    db=db,
                    raised=raised,
                    committed=not raised,
                )
            return result

        def traced_call_button(self_ctrl, model, method, args, kwargs, path=None):
            uid = getattr(getattr(self_ctrl, "env", None), "uid", None)
            db = getattr(getattr(self_ctrl, "env", None), "cr", None)
            db = getattr(db, "dbname", None) if db else None
            raised = False
            try:
                result = original_call_button(self_ctrl, model, method, args, kwargs, path=path)
            except Exception:
                raised = True
                raise
            finally:
                tracer.record(
                    route="/web/dataset/call_button",
                    model=model,
                    method=method,
                    args=args,
                    uid=uid,
                    db=db,
                    raised=raised,
                    committed=not raised,
                )
            return result

        dataset_controller_cls.call_kw = traced_call_kw
        dataset_controller_cls.call_button = traced_call_button
        self._originals["call_kw"] = original_call_kw
        self._originals["call_button"] = original_call_button
        self._originals["cls"] = dataset_controller_cls

        # -- Layer 2: odoo.service.model.execute_cr patch ------------------
        if model_service_module is not None:
            self.install_execute_cr(model_service_module)

    def install_execute_cr(self, model_service_module: Any) -> None:
        """Patch ``odoo.service.model.execute_cr`` to capture all ORM
        dispatch including custom controller routes.

        Can be called standalone (without ``install()``) for setups
        that don't need DataSet controller patches.
        """
        if "execute_cr" in self._originals:
            return  # already installed

        tracer = self
        original_execute_cr = model_service_module.execute_cr

        def traced_execute_cr(cr, uid, obj, method, args, kw):
            db = getattr(cr, "dbname", None)
            raised = False
            try:
                result = original_execute_cr(cr, uid, obj, method, args, kw)
            except Exception:
                raised = True
                raise
            finally:
                import threading as _threading
                tl = getattr(model_service_module, "thread_local", _threading.local())
                route = getattr(tl, "_benchmark_route", f"execute_cr:{obj}.{method}")
                tracer.record(
                    route=route,
                    controller_type="orm",
                    model=obj,
                    method=method,
                    args=args,
                    uid=uid,
                    db=db,
                    raised=raised,
                    committed=not raised,
                )
            return result

        model_service_module.execute_cr = traced_execute_cr
        self._originals["execute_cr"] = original_execute_cr
        self._originals["model_service_module"] = model_service_module

    def install_orm_hooks(self, base_model_cls: type) -> None:
        """Patch ``BaseModel.create/write/unlink`` to capture ORM writes
        that bypass both ``DataSet`` and ``execute_cr``.

        This is Layer 3 — it captures direct ORM calls made by custom
        controllers such as ``/website/form/<model>`` which use
        ``request.env[model].create(values)`` without going through the
        RPC dispatch layer.

        Args:
            base_model_cls: ``odoo.models.BaseModel`` class.
        """
        tracer = self

        import functools

        for method_name in ("create", "write", "unlink"):
            original = getattr(base_model_cls, method_name)

            def _make_hook(orig: Any, mname: str) -> Any:
                def hook(self_model: Any, *args: Any, **kwargs: Any) -> Any:
                    model_name = getattr(self_model, "_name", "unknown")
                    uid = getattr(getattr(self_model, "env", None), "uid", None)
                    db = getattr(getattr(getattr(self_model, "env", None), "cr", None), "dbname", None)

                    # Try to detect the HTTP route context so we can
                    # emit custom:/path entries for custom controllers.
                    http_route = None
                    try:
                        from odoo.http import request as http_req
                        if http_req and hasattr(http_req, "httprequest"):
                            http_route = http_req.httprequest.path
                    except Exception:
                        pass

                    # Skip ORM-level tracing for requests that are
                    # already captured by the DataSet controller patches
                    # (Layer 1) to avoid double-counting.
                    is_dataset_route = (
                        http_route is not None
                        and "/web/dataset/" in http_route
                    )

                    raised = False
                    try:
                        return orig(self_model, *args, **kwargs)
                    except Exception:
                        raised = True
                        raise
                    finally:
                        if not is_dataset_route:
                            if http_route:
                                # Custom HTTP controller route — emit a
                                # single custom:/route entry (not both
                                # orm: and custom: to avoid double-counting)
                                custom_route = http_route
                                if model_name not in http_route:
                                    custom_route = f"{http_route}/{model_name}"
                                tracer.record(
                                    route=f"custom:{custom_route}",
                                    controller_type="custom_http",
                                    model=model_name,
                                    method=mname,
                                    args=args,
                                    uid=uid,
                                    db=db,
                                    raised=raised,
                                    committed=not raised,
                                )
                            else:
                                # Direct ORM call (no HTTP context)
                                tracer.record(
                                    route=f"orm:{model_name}.{mname}",
                                    controller_type="orm_direct",
                                    model=model_name,
                                    method=mname,
                                    args=args,
                                    uid=uid,
                                    db=db,
                                    raised=raised,
                                    committed=not raised,
                                )
                # Preserve Odoo API decorator metadata (_api_model,
                # _readonly, etc.) so call_kw() dispatch still works.
                functools.update_wrapper(hook, orig)
                for attr in ("_api_model", "_readonly", "_api"):
                    if hasattr(orig, attr):
                        setattr(hook, attr, getattr(orig, attr))
                return hook

            setattr(base_model_cls, method_name, _make_hook(original, method_name))
            self._originals[f"orm_{method_name}"] = original

        self._originals["base_model_cls"] = base_model_cls

    def uninstall(self) -> None:
        """Restore original controller methods and functions."""
        cls = self._originals.get("cls")
        if cls is not None:
            if "call_kw" in self._originals:
                cls.call_kw = self._originals["call_kw"]
            if "call_button" in self._originals:
                cls.call_button = self._originals["call_button"]

        msm = self._originals.get("model_service_module")
        if msm is not None and "execute_cr" in self._originals:
            msm.execute_cr = self._originals["execute_cr"]

        bmc = self._originals.get("base_model_cls")
        if bmc is not None:
            for method_name in ("create", "write", "unlink"):
                key = f"orm_{method_name}"
                if key in self._originals:
                    setattr(bmc, method_name, self._originals[key])

        self._originals.clear()
