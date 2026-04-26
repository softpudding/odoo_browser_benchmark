#!/usr/bin/env python3
"""Benchmark wrapper for OpenBrowser (https://github.com/softpudding/OpenBrowser).

Setup:
    1. Start OpenBrowser server: cd OpenBrowser/server && python main.py start
    2. Connect Chrome with the OpenBrowser extension
    3. Set OPENBROWSER_CHROME_UUID to the browser's UUID token

    Set OPENBROWSER_URL (default: http://127.0.0.1:8765).
    Uses DashScope/Qwen models natively (no OpenAI mapping needed).

Usage:
    uv run benchmark-eval run <task> --agent command \
        --cmd "python benchmark/agents/run_openbrowser.py"
"""

import atexit
import json
import os
import re
import signal
import sys
import tempfile
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from _env_setup import get_env, build_instruction


def request_json(url, method="GET", body=None, timeout=10):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def cleanup_conversation(server_url, chrome_uuid, conversation_id, lane_port=None):
    """Close the conversation's tabs and DELETE the session.

    Mirrors _cleanup_openbrowser_conversation in
    OpenBrowser/eval/evaluate_browser_agent.py, with one important
    correction: the OpenBrowser extension only registers a tab as
    "managed" when certain tool calls hit it (highlight, switch).
    A tab the agent navigates to via TabAction("init") often stays
    `isManaged: false`, and Odoo's auth redirects spawn extra tabs
    that are never registered. So filtering by ``managed_only=true``
    misses most of the conversation's actual tabs and leaks them.

    We instead list all tabs in the browser (managed_only=false) and
    close every tab whose URL contains our lane host
    ``lane-<lane_port>.localtest.me`` — which is unique per run by
    construction, so we can't accidentally nuke another lane's tabs.
    """
    if not conversation_id or not chrome_uuid:
        return

    tabs = []
    try:
        params = urllib.parse.urlencode({
            "browser_id": chrome_uuid,
            "conversation_id": conversation_id,
            "managed_only": "false",
        })
        req = urllib.request.Request(
            f"{server_url}/tabs?{params}", method="GET"
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode())
        if data.get("success"):
            tabs = data.get("data", {}).get("tabs", []) or []
    except Exception as e:
        print(f"[cleanup] list tabs failed: {e}", file=sys.stderr)

    if lane_port:
        lane_host = f"lane-{lane_port}.localtest.me"
        tabs = [t for t in tabs if lane_host in (t.get("url") or "")]
    else:
        # Fallback: only close tabs the extension flagged as managed
        # under our conversation. Loses unmanaged tabs but at least
        # safe across lanes.
        tabs = [t for t in tabs if t.get("isManaged")]

    # Close tabs in parallel — under K=5 contention each close round-
    # trip can take 2-3s, and we may have 10+ tabs. Serial close with
    # a 2s per-call timeout was repeatedly timing out and leaking tabs.
    from concurrent.futures import ThreadPoolExecutor

    def _close_one(tab):
        # The /tabs API returns the tab id under "id" — NOT under
        # "tabId"/"tab_id" as evaluate_browser_agent.py assumed. Without
        # this we silently no-op on every close (lookup fails, returns
        # tab_id=None, error path skips print, closed counter stays 0).
        tab_id = tab.get("id")
        if not isinstance(tab_id, int):
            tab_id = tab.get("tabId")
        if not isinstance(tab_id, int):
            tab_id = tab.get("tab_id")
        if not isinstance(tab_id, int):
            return False, None, f"missing tab id in {tab!r}"
        params = urllib.parse.urlencode({
            "action": "close",
            "browser_id": chrome_uuid,
            "conversation_id": conversation_id,
            "tab_id": str(tab_id),
        })
        try:
            req = urllib.request.Request(
                f"{server_url}/tabs?{params}", data=b"", method="POST"
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                resp.read()
            return True, tab_id, None
        except Exception as e:
            return False, tab_id, str(e)

    closed = 0
    if tabs:
        # In the atexit path the interpreter is shutting down and
        # ThreadPoolExecutor.submit raises RuntimeError. Try parallel
        # first; on shutdown error fall back to serial.
        results = []
        try:
            with ThreadPoolExecutor(max_workers=min(8, len(tabs))) as pool:
                results = list(pool.map(_close_one, tabs))
        except RuntimeError as e:
            print(f"[cleanup] parallel close unavailable ({e}), "
                  "falling back to serial", file=sys.stderr, flush=True)
            results = [_close_one(t) for t in tabs]
        for ok, tab_id, err in results:
            if ok:
                closed += 1
            else:
                print(f"[cleanup] close tab {tab_id} failed: {err}",
                      file=sys.stderr, flush=True)

    print(f"[cleanup] closed {closed}/{len(tabs)} lane-host tabs", flush=True)

    # Debug escape hatch: skip the conversation DELETE so the session
    # record survives in ~/.openbrowser/sessions.db for post-hoc inspection.
    # Tab cleanup above still runs (that's what prevents Chrome OOM).
    if os.environ.get("BENCHMARK_KEEP_CONVERSATION") == "1":
        print(
            f"[cleanup] keeping conversation {conversation_id} "
            "(BENCHMARK_KEEP_CONVERSATION=1)",
            flush=True,
        )
        return

    try:
        req = urllib.request.Request(
            f"{server_url}/agent/conversations/{conversation_id}",
            method="DELETE",
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            resp.read()
        print(f"[cleanup] conversation {conversation_id} deleted", flush=True)
    except Exception as e:
        print(f"[cleanup] delete conversation failed: {e}", file=sys.stderr)


def _install_sigterm_to_sysexit():
    """Convert SIGTERM into sys.exit so atexit + finally cleanup fire.

    formal_run.py sends SIGTERM after the 900s outer timeout, then
    SIGKILL 10s later. Without this handler the default SIGTERM action
    kills the process without running finally blocks, leaking the
    conversation and managed tabs.
    """
    def _handler(signum, frame):
        sys.exit(128 + signum)
    signal.signal(signal.SIGTERM, _handler)


def _install_wallclock_watchdog(seconds):
    """Trigger a clean SystemExit at ``seconds`` so finally + atexit
    cleanup runs *before* eval.py's harder ``subprocess.run(timeout=600)``
    SIGKILL fires.

    eval.py launches the wrapper as a subprocess with a 600s timeout.
    On timeout it sends SIGKILL — bypassing every Python-level cleanup
    hook. The result: when the agent is still running at 600s (the
    common case for hard tasks), tabs and the OpenBrowser conversation
    leak. Setting a SIGALRM at 580s gives us 20s to close tabs and
    DELETE the conversation cleanly.
    """
    def _handler(signum, frame):
        sys.stderr.write(
            f"[watchdog] {seconds}s wall-clock budget exhausted, "
            "exiting cleanly so cleanup runs\n"
        )
        sys.stderr.flush()
        sys.exit(124)
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(seconds)


_PER_LANE_HOST_RE = re.compile(r"127\.0\.0\.1:(\d+)")


def per_lane_host_rewrite(text: str) -> str:
    """Rewrite ``127.0.0.1:<port>`` to ``lane-<port>.localtest.me:<port>``.

    Each per-run Odoo binds to ``127.0.0.1`` on a unique port. When
    multiple lanes share one Chrome browser, the cookie jar is keyed
    by host (port-blind), so every lane writes/reads the same
    ``session_id`` cookie and CSRF tokens collide. Routing each lane
    through a unique ``*.localtest.me`` subdomain (public DNS, all
    pointing back at 127.0.0.1) gives every lane its own cookie scope
    while leaving the wire path unchanged.

    Disable with ``BENCHMARK_PER_LANE_HOST=0`` for local debugging.
    """
    if os.environ.get("BENCHMARK_PER_LANE_HOST", "1") != "1":
        return text
    return _PER_LANE_HOST_RE.sub(r"lane-\1.localtest.me:\1", text)


def main():
    _install_sigterm_to_sysexit()
    _install_wallclock_watchdog(
        int(os.environ.get("OPENBROWSER_WALLCLOCK_BUDGET", "580"))
    )
    full_instruction = per_lane_host_rewrite(build_instruction())
    # Extract our lane port for cleanup matching: post-rewrite the
    # instruction has lane-<port>.localtest.me URLs, where port is
    # the per-run Odoo port — unique to this run.
    _lane_match = re.search(r"lane-(\d+)\.localtest\.me", full_instruction)
    lane_port = _lane_match.group(1) if _lane_match else None
    server_url = os.environ.get("OPENBROWSER_URL", "http://127.0.0.1:8765")
    chrome_uuid = os.environ.get("OPENBROWSER_CHROME_UUID", "")
    # The frontend always passes model_alias + cwd; without them the
    # server falls back to a default profile that caps the agent at ~20
    # turns, terminating it long before complex tasks finish.
    model_alias = os.environ.get("OPENBROWSER_MODEL_ALIAS", "qwen36plus")
    # Fresh tempdir per run so the agent can't see / modify the
    # benchmark repo via its terminal/file_editor tools. Don't auto-clean
    # so any artifacts the agent wrote remain inspectable.
    cwd = os.environ.get("OPENBROWSER_CWD") or tempfile.mkdtemp(
        prefix="openbrowser_cwd_"
    )

    if not chrome_uuid:
        print("ERROR: OPENBROWSER_CHROME_UUID not set", file=sys.stderr)
        print("Set it in env or ~/.zshrc after connecting Chrome with the extension", file=sys.stderr)
        sys.exit(1)

    # Verify server and browser connection
    try:
        status = request_json(f"{server_url}/api")
        if not status.get("websocket_connected"):
            print("ERROR: Chrome extension not connected to OpenBrowser server", file=sys.stderr)
            sys.exit(1)

        validity = request_json(f"{server_url}/browsers/{chrome_uuid}/valid")
        if not validity.get("valid"):
            print(f"ERROR: Browser UUID {chrome_uuid} is not valid", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cannot reach OpenBrowser server: {e}", file=sys.stderr)
        sys.exit(1)

    # Create a conversation. Match the frontend exactly: include
    # cwd + model_alias so the server selects the configured profile
    # (turn budget, system-prompt blocks, etc.) instead of a default
    # that caps the agent at ~20 turns.
    #
    # Also forward $DASHSCOPE_BASE_URL as the conversation's `base_url`.
    # OpenBrowser ignores the env var for its own LLM client, so without
    # passing it explicitly here all DashScope traffic bypasses the
    # benchmark's per-run mitmdump proxy and tokens always come out
    # zero in the queue.
    body = {
        "browser_id": chrome_uuid,
        "cwd": cwd,
        "model_alias": model_alias,
    }
    base_url_override = os.environ.get("DASHSCOPE_BASE_URL")
    if base_url_override:
        body["base_url"] = base_url_override
    conv_data = request_json(
        f"{server_url}/agent/conversations",
        method="POST",
        body=body,
    )
    conversation_id = conv_data["conversation_id"]
    print(
        f"[conversation] {conversation_id} model_alias={model_alias} "
        f"base_url={base_url_override or '(server default)'}",
        flush=True,
    )

    # Belt-and-suspenders: finally is the primary cleanup path; atexit
    # catches sys.exit() (including the SIGTERM->sys.exit converter).
    atexit.register(
        cleanup_conversation, server_url, chrome_uuid, conversation_id, lane_port
    )

    # Send the task via SSE streaming
    payload = json.dumps({
        "text": full_instruction,
        "cwd": cwd,
        "browser_id": chrome_uuid,
    }).encode()
    req = urllib.request.Request(
        f"{server_url}/agent/conversations/{conversation_id}/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )

    completed = False
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            sse_event = None
            sse_data = None
            for raw_line in resp:
                line = raw_line.decode("utf-8").rstrip("\n")
                if not line:
                    # End of SSE event
                    if sse_event and sse_data:
                        try:
                            data = json.loads(sse_data)
                        except json.JSONDecodeError:
                            data = {"raw": sse_data}

                        event_type = data.get("type", sse_event)
                        # Print key events
                        if event_type in ("MessageEvent", "message"):
                            text = data.get("text", data.get("message", ""))
                            print(f"[message] {text[:200]}", flush=True)
                        elif event_type in ("ActionEvent", "action"):
                            action = data.get("action", data)
                            print(f"[action] {json.dumps(action)[:200]}", flush=True)
                        elif event_type in ("ThoughtEvent", "thought"):
                            print(f"[thought] {data.get('thought', '')[:200]}", flush=True)
                        elif event_type == "complete":
                            print(f"[complete] {data.get('message', '')}", flush=True)
                            completed = True

                    sse_event = None
                    sse_data = None
                    continue

                if line.startswith("event:"):
                    sse_event = line[6:].strip()
                elif line.startswith("data:"):
                    sse_data = line[5:].lstrip()

    except Exception as e:
        print(f"OpenBrowser streaming error: {e}", file=sys.stderr)
    finally:
        cleanup_conversation(server_url, chrome_uuid, conversation_id, lane_port)

    if completed:
        print("OpenBrowser: task completed")
        sys.exit(0)
    else:
        # Task may have completed even without "complete" event
        print("OpenBrowser: stream ended without explicit completion signal")
        sys.exit(0)  # Exit 0 — let eval.py judge by DB state


if __name__ == "__main__":
    main()
