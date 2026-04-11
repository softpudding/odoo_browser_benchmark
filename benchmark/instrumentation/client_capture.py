"""Client-side network capture — Section 8.1 of the spec.

Uses CDP (Chrome DevTools Protocol) via Playwright to intercept all
browser-originated XHR / fetch / JSON-RPC requests during an episode.

Usage::

    capture = ClientCapture()
    await capture.install(page)   # Playwright page
    # ... run agent episode ...
    entries = capture.get_entries()
"""

from __future__ import annotations

import hashlib
import threading
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class ClientEntry:
    """A single captured client-side network request."""
    timestamp: float
    method: str  # HTTP method
    url: str
    request_body_hash: str
    response_status: int | None = None
    response_body_hash: str | None = None
    frame_id: str | None = None
    resource_type: str | None = None  # xhr, fetch, document, etc.

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "method": self.method,
            "url": self.url,
            "request_body_hash": self.request_body_hash,
            "response_status": self.response_status,
            "response_body_hash": self.response_body_hash,
            "frame_id": self.frame_id,
            "resource_type": self.resource_type,
        }


def _hash_body(body: str | bytes | None) -> str:
    if body is None:
        return ""
    if isinstance(body, str):
        body = body.encode("utf-8")
    return hashlib.sha256(body).hexdigest()[:16]


class ClientCapture:
    """Captures browser network requests via Playwright request/response events."""

    def __init__(self) -> None:
        self._entries: list[ClientEntry] = []
        self._lock = threading.Lock()
        self._pending: dict[str, ClientEntry] = {}  # keyed by request URL+method

    def install_sync(self, page: Any) -> None:
        """Install capture on a *synchronous* Playwright page.

        Safe to call multiple times — previous listeners and entries are
        cleared first.

        Hooks ``page.on("request", ...)`` and ``page.on("response", ...)``.
        """
        # Remove previous listeners if reinstalling on the same page
        if hasattr(self, "_handlers") and hasattr(self, "_page"):
            try:
                self._page.remove_listener("request", self._handlers[0])
                self._page.remove_listener("response", self._handlers[1])
            except Exception:
                pass
        self.clear()

        capture = self

        def on_request(request: Any) -> None:
            try:
                body = request.post_data
            except Exception:
                body = None
            entry = ClientEntry(
                timestamp=time.time(),
                method=request.method,
                url=request.url,
                request_body_hash=_hash_body(body),
                frame_id=getattr(request.frame, "name", None),
                resource_type=request.resource_type,
            )
            key = f"{request.method}:{request.url}:{id(request)}"
            with capture._lock:
                capture._pending[key] = entry
                capture._entries.append(entry)

        def on_response(response: Any) -> None:
            key = f"{response.request.method}:{response.request.url}:{id(response.request)}"
            with capture._lock:
                entry = capture._pending.pop(key, None)
            if entry is not None:
                entry.response_status = response.status
                try:
                    body = response.body()
                    entry.response_body_hash = _hash_body(body)
                except Exception:
                    pass

        page.on("request", on_request)
        page.on("response", on_response)
        self._page = page
        self._handlers = (on_request, on_response)

    async def install_async(self, page: Any) -> None:
        """Install capture on an *async* Playwright page."""
        capture = self

        def on_request(request: Any) -> None:
            try:
                body = request.post_data
            except Exception:
                body = None
            entry = ClientEntry(
                timestamp=time.time(),
                method=request.method,
                url=request.url,
                request_body_hash=_hash_body(body),
                frame_id=getattr(request.frame, "name", None),
                resource_type=request.resource_type,
            )
            key = f"{request.method}:{request.url}:{id(request)}"
            with capture._lock:
                capture._pending[key] = entry
                capture._entries.append(entry)

        def on_response(response: Any) -> None:
            key = f"{response.request.method}:{response.request.url}:{id(response.request)}"
            with capture._lock:
                entry = capture._pending.pop(key, None)
            if entry is not None:
                entry.response_status = response.status

        page.on("request", on_request)
        page.on("response", on_response)
        self._page = page
        self._handlers = (on_request, on_response)

    def get_entries(self) -> list[dict[str, Any]]:
        """Return all captured entries as dicts."""
        with self._lock:
            return [e.to_dict() for e in self._entries]

    def get_jsonrpc_entries(self) -> list[dict[str, Any]]:
        """Return only JSON-RPC POST entries (to ``/web/dataset/`` etc.)."""
        with self._lock:
            return [
                e.to_dict() for e in self._entries
                if e.method == "POST" and (
                    "/web/dataset/" in e.url
                    or "/jsonrpc" in e.url
                    or e.resource_type in ("xhr", "fetch")
                )
            ]

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._pending.clear()
