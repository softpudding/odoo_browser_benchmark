#!/usr/bin/env python3
"""Benchmark wrapper for Agent-E (https://github.com/EmergenceAI/Agent-E).

Setup:
    git clone https://github.com/EmergenceAI/Agent-E.git
    cd Agent-E && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    # Start server in its own venv:
    PYTHONPATH=. .venv/bin/python3 -c "from ae.server.api_routes import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"

    Set AGENT_E_URL to point to the running server (default: http://127.0.0.1:8000).

    IMPORTANT: Start the server with nest_asyncio + asyncio loop (not uvloop):
        cd Agent-E && PYTHONPATH=. .venv/bin/python3 -c "
            import nest_asyncio; nest_asyncio.apply()
            import asyncio; asyncio.set_event_loop_policy(None)
            from ae.server.api_routes import app
            import uvicorn
            uvicorn.run(app, host='0.0.0.0', port=8000, loop='asyncio')
        "

Usage:
    uv run benchmark-eval run <task> --agent command \
        --cmd "python benchmark/agents/run_agent_e.py"
"""

import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from _env_setup import setup_openai_compat, build_instruction

setup_openai_compat()


def main():
    full_instruction = build_instruction()
    agent_e_url = os.environ.get("AGENT_E_URL", "http://127.0.0.1:8000")

    payload = json.dumps({"command": full_instruction}).encode()
    req = urllib.request.Request(
        f"{agent_e_url}/execute_task",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            # Agent-E returns a StreamingResponse — read it chunk by chunk
            last_data = ""
            final_result = None
            for line in resp:
                text = line.decode("utf-8", errors="replace").strip()
                if not text:
                    continue
                print(text, flush=True)
                last_data = text

                # Look for completion signals in the streamed data
                if "TERMINATE" in text or "completed" in text.lower():
                    final_result = "completed"

            if final_result == "completed":
                print("Agent-E: task completed")
                sys.exit(0)
            else:
                print(f"Agent-E: task may not have completed. Last output: {last_data[:200]}")
                sys.exit(1)

    except Exception as e:
        print(f"Agent-E error: {e}", file=sys.stderr)
        print("Make sure Agent-E server is running", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
