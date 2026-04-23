#!/usr/bin/env python3
"""mitmproxy addon + CLI to log LLM token usage from DashScope / OpenAI-compat
traffic to a JSONL file, and summarize totals.

Proxy (run in front of the agent):

    mitmdump --mode reverse:https://dashscope.aliyuncs.com/compatible-mode/v1 \\
        -p 8765 --set stream_large_bodies=0 \\
        --set token_log=/tmp/tokens.jsonl \\
        -s benchmark/agents/token_logger.py

Then point each agent at the proxy::

    export DASHSCOPE_BASE_URL=http://127.0.0.1:8765

Summarize a JSONL file::

    python benchmark/agents/token_logger.py summarize /tmp/tokens.jsonl \\
        --out /path/to/output_dir/token_usage.json
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


USAGE_PATHS = ("/chat/completions", "/responses", "/messages")


def _normalize(usage: dict) -> dict:
    prompt = usage.get("prompt_tokens") or usage.get("input_tokens", 0) or 0
    completion = usage.get("completion_tokens") or usage.get("output_tokens", 0) or 0
    total = usage.get("total_tokens") or (prompt + completion)
    out = {
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": total,
    }
    details = usage.get("completion_tokens_details") or usage.get("output_tokens_details")
    if isinstance(details, dict) and details.get("reasoning_tokens") is not None:
        out["reasoning_tokens"] = details["reasoning_tokens"]
    cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens")
    if cached:
        out["cached_tokens"] = cached
    return out


def _extract_usage(body: bytes, content_type: str) -> dict | None:
    text = body.decode("utf-8", errors="replace")
    if "event-stream" in content_type.lower():
        usage = None
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload or payload == "[DONE]":
                continue
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            u = chunk.get("usage")
            if isinstance(u, dict):
                usage = u
        return _normalize(usage) if usage else None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return None
    u = obj.get("usage") if isinstance(obj, dict) else None
    return _normalize(u) if u else None


# ---------------------------------------------------------------------------
# mitmproxy addon
# ---------------------------------------------------------------------------
def load(loader):  # pragma: no cover - invoked by mitmproxy
    loader.add_option(
        name="token_log",
        typespec=str,
        default="/tmp/tokens.jsonl",
        help="JSONL file to append per-request token usage entries",
    )


def response(flow) -> None:  # pragma: no cover - invoked by mitmproxy
    if not any(p in flow.request.path for p in USAGE_PATHS):
        return
    content_type = flow.response.headers.get("Content-Type", "")
    usage = _extract_usage(flow.response.content, content_type)
    if not usage:
        return
    from mitmproxy import ctx  # imported lazily so CLI mode doesn't need mitmproxy

    entry = {
        "ts": time.time(),
        "path": flow.request.path,
        "status": flow.response.status_code,
        **usage,
    }
    log_path = Path(ctx.options.token_log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Summarize CLI
# ---------------------------------------------------------------------------
def summarize(log_path: str) -> dict:
    summary = {
        "requests": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "reasoning_tokens": 0,
        "cached_tokens": 0,
    }
    path = Path(log_path)
    if not path.exists():
        return summary
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        summary["requests"] += 1
        for k in ("prompt_tokens", "completion_tokens", "total_tokens", "reasoning_tokens", "cached_tokens"):
            summary[k] += entry.get(k, 0) or 0
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("summarize", help="Sum a tokens.jsonl into one JSON blob")
    s.add_argument("log")
    s.add_argument("--out", help="Write JSON summary here (default: stdout only)")

    args = ap.parse_args()
    if args.cmd == "summarize":
        summary = summarize(args.log)
        text = json.dumps(summary, indent=2)
        if args.out:
            Path(args.out).write_text(text + "\n")
        print(text)


if __name__ == "__main__":
    main()
