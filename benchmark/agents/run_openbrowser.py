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


def cleanup_conversation(server_url, chrome_uuid, conversation_id):
    """Close managed tabs and delete the conversation.

    Mirrors _cleanup_openbrowser_conversation in
    OpenBrowser/eval/evaluate_browser_agent.py. Without this, every run
    leaks one conversation in the OpenBrowser server and one tab group
    in the persistent Chrome — accumulating to OOM after a few hundred
    benchmark runs.
    """
    if not conversation_id or not chrome_uuid:
        return

    tabs = []
    try:
        params = urllib.parse.urlencode({
            "browser_id": chrome_uuid,
            "conversation_id": conversation_id,
            "managed_only": "true",
        })
        req = urllib.request.Request(
            f"{server_url}/tabs?{params}", method="GET"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        if data.get("success"):
            tabs = data.get("data", {}).get("tabs", []) or []
    except Exception as e:
        print(f"[cleanup] list tabs failed: {e}", file=sys.stderr)

    closed = 0
    for tab in tabs:
        tab_id = tab.get("tabId")
        if not isinstance(tab_id, int):
            tab_id = tab.get("tab_id")
        if not isinstance(tab_id, int):
            continue
        try:
            params = urllib.parse.urlencode({
                "action": "close",
                "browser_id": chrome_uuid,
                "conversation_id": conversation_id,
                "tab_id": str(tab_id),
            })
            req = urllib.request.Request(
                f"{server_url}/tabs?{params}", data=b"", method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read()
            closed += 1
        except Exception as e:
            print(f"[cleanup] close tab {tab_id} failed: {e}", file=sys.stderr)

    print(f"[cleanup] closed {closed}/{len(tabs)} managed tabs", flush=True)

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
        with urllib.request.urlopen(req, timeout=5) as resp:
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


def main():
    _install_sigterm_to_sysexit()
    full_instruction = build_instruction()
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
    atexit.register(cleanup_conversation, server_url, chrome_uuid, conversation_id)

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
        cleanup_conversation(server_url, chrome_uuid, conversation_id)

    if completed:
        print("OpenBrowser: task completed")
        sys.exit(0)
    else:
        # Task may have completed even without "complete" event
        print("OpenBrowser: stream ended without explicit completion signal")
        sys.exit(0)  # Exit 0 — let eval.py judge by DB state


if __name__ == "__main__":
    main()
