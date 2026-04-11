"""Runner guard — agent contract enforcement (Section 7.3).

Ensures that browser-only agents do not violate the benchmark contract
by making direct HTTP calls, database access, or other forbidden actions.

The guard wraps a Playwright page to intercept and block forbidden patterns.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

# Patterns that indicate direct RPC / API calls outside the browser context.
# These are blocked for ``browser_only`` agents.
_FORBIDDEN_URL_PATTERNS = [
    re.compile(r"/jsonrpc$"),         # direct JSON-RPC endpoint
    re.compile(r"/xmlrpc/"),          # XML-RPC
]

# Routes that are only valid when initiated from the browser page context.
# Direct programmatic access to these is forbidden.
_DIRECT_ACCESS_ROUTES = frozenset({
    "/web/dataset/call_kw",
    "/web/dataset/call_button",
})


@dataclass
class Violation:
    """A single contract violation."""
    timestamp: float
    kind: str       # "direct_rpc" | "direct_db" | "oracle_read" | "forbidden_action"
    detail: str
    blocked: bool   # whether the guard blocked the action


class RunnerGuard:
    """Enforces the agent interface contract during a benchmark run.

    For ``browser_only`` tasks, the guard ensures:
    - No direct HTTP calls to Odoo endpoints outside browser page context
    - No direct JSON-RPC construction and submission
    - No direct database access
    - No reading of benchmark oracle files
    """

    def __init__(
        self,
        agent_interface: str = "browser_only",
        task_dir: str | None = None,
    ) -> None:
        self.agent_interface = agent_interface
        self.task_dir = task_dir
        self.violations: list[Violation] = []
        self._active = False

    def start(self) -> None:
        self._active = True
        self.violations.clear()

    def stop(self) -> None:
        self._active = False

    def check_request(self, method: str, url: str, *, from_browser: bool = True) -> bool:
        """Check if a request is allowed under the agent contract.

        Returns True if allowed, False if blocked.
        """
        if not self._active:
            return True

        if self.agent_interface != "browser_only":
            return True

        # Browser-initiated requests are always allowed
        if from_browser:
            return True

        # Block direct RPC calls from agent code
        for pattern in _FORBIDDEN_URL_PATTERNS:
            if pattern.search(url):
                self._record_violation(
                    "direct_rpc",
                    f"Direct RPC call blocked: {method} {url}",
                    blocked=True,
                )
                return False

        # Block direct access to dataset routes
        for route in _DIRECT_ACCESS_ROUTES:
            if route in url:
                self._record_violation(
                    "direct_rpc",
                    f"Direct dataset route access blocked: {method} {url}",
                    blocked=True,
                )
                return False

        return True

    def check_file_access(self, path: str) -> bool:
        """Check if file access is allowed (blocks oracle file reads)."""
        if not self._active:
            return True

        if self.agent_interface != "browser_only":
            return True

        # Block reading oracle files during task execution
        oracle_patterns = ["trace_spec.yaml", "state_spec.yaml", "task.yaml"]
        if self.task_dir and any(p in path for p in oracle_patterns):
            self._record_violation(
                "oracle_read",
                f"Oracle file read blocked: {path}",
                blocked=True,
            )
            return False

        return True

    def check_db_access(self, operation: str) -> bool:
        """Check if direct database access is allowed."""
        if not self._active:
            return True

        if self.agent_interface != "browser_only":
            return True

        self._record_violation(
            "direct_db",
            f"Direct DB access blocked: {operation}",
            blocked=True,
        )
        return False

    def _record_violation(self, kind: str, detail: str, blocked: bool) -> None:
        import time
        self.violations.append(Violation(
            timestamp=time.time(),
            kind=kind,
            detail=detail,
            blocked=blocked,
        ))

    def get_violations(self) -> list[dict[str, Any]]:
        return [
            {
                "timestamp": v.timestamp,
                "kind": v.kind,
                "detail": v.detail,
                "blocked": v.blocked,
            }
            for v in self.violations
        ]

    def has_violations(self) -> bool:
        return len(self.violations) > 0

    def install_on_page(self, page: Any) -> None:
        """Install route interception on a Playwright page (sync API).

        Intercepts requests to raw RPC endpoints and direct form POST
        endpoints. These are always blocked and logged as violations
        because in the ``browser_only`` track, programmatic RPCs and
        direct HTTP form submissions are forbidden.

        Note on ``/web/dataset/*``: these routes are used by Odoo's own
        UI JS framework for every normal interaction (clicks, form saves,
        etc.), so they cannot be blocked at the Playwright routing level
        without breaking the UI entirely. Protection against agent abuse
        of dataset routes relies on the server-side tracer: all operations
        are captured and scored via ``forbidden_ops``, ``HarmfulWriteRate``,
        and ``StrictSuccess``.
        """
        if self.agent_interface != "browser_only":
            return

        guard = self
        self._page = page
        self._route_patterns: list[str] = []

        def handle_route(route: Any) -> None:
            request = route.request
            guard._record_violation(
                "direct_rpc",
                f"Programmatic RPC blocked: {request.method} {request.url}",
                blocked=True,
            )
            route.abort("blockedbyclient")

        # Raw RPC endpoints (never used by normal Odoo UI).
        #
        # Design note: /web/dataset/call_kw and /web/dataset/call_button
        # are NOT intercepted because Odoo's UI JS framework uses them
        # for every normal interaction (clicks, form saves, etc.).
        # Playwright page.route() cannot distinguish UI-triggered vs
        # agent-injected fetch() calls to these endpoints.
        #
        # /website/form/* is also NOT intercepted because Odoo's form
        # widget submits via fetch().
        #
        # Enforcement against direct RPC abuse relies on:
        # 1. Server-side tracer capturing ALL backend operations
        # 2. forbidden_ops in trace_spec flagging unauthorized writes
        # 3. HarmfulWriteRate and StrictSuccess metrics penalizing abuse
        # 4. Oracle file protection preventing agents from reading specs
        #
        # This is the intended enforcement model per Section 7.3 of the
        # spec: the browser-only contract is enforced through scoring,
        # not solely through request blocking.
        for pattern in ("**/jsonrpc", "**/xmlrpc/**"):
            page.route(pattern, handle_route)
            self._route_patterns.append(pattern)

        self._handle_route = handle_route

    def uninstall_from_page(self) -> None:
        """Remove route interceptions from the Playwright page.

        Must be called when the run finishes to avoid poisoning
        subsequent runs that reuse the same page.
        """
        page = getattr(self, "_page", None)
        if page is None:
            return
        for pattern in getattr(self, "_route_patterns", []):
            try:
                # Unroute without specifying handler removes all handlers
                page.unroute(pattern)
            except Exception:
                pass
        self._page = None
        self._route_patterns = []
