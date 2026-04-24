#!/usr/bin/env python3
"""Background sweeper for orphaned browser processes.

Each benchmark run launches playwright-bundled Chrome for Testing (and
skyvern launches its own Chrome instance under `temp/skyvern_browser_*`).
When an agent dies ungracefully — timeout hit, subprocess killed, wrapper
crash — the Chrome main process often dies but its `chrome_crashpad_handler`
helpers (deliberately detached from the parent to survive crashes and
collect minidumps) stay running with PPID=1. At scale this eats FDs and
memory.

This reaper watches for benchmark-browser processes whose parent is PID 1
(i.e. truly orphaned) and SIGKILLs them. It deliberately does NOT touch
processes with a live parent — those belong to currently-running agent
lanes.

Run alongside the formal_run dispatcher:

    python benchmark/agents/browser_reaper.py --interval 30

It will log every reap to stderr and exit on SIGINT.
"""
from __future__ import annotations

import argparse
import os
import re
import signal
import subprocess
import sys
import time


BROWSER_SIGNATURES = (
    "Chrome for Testing",          # playwright-bundled chromium
    "ms-playwright/chromium",      # cache path for the binary + helpers
    "/temp/skyvern_browser_",      # skyvern's own Chrome instance
    "browser_use_local.py",        # browser-use wrapper can also orphan
    "playwright/driver/node",      # playwright driver itself
)


def find_orphaned_pids() -> list[tuple[int, str]]:
    """Return [(pid, cmd_preview), ...] for benchmark-browser processes
    whose PPID == 1 (truly detached from the launching agent)."""
    out = subprocess.check_output(
        ["ps", "-eo", "pid=,ppid=,command="], text=True
    )
    orphans = []
    for line in out.splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+)\s+(.*)", line)
        if not m:
            continue
        pid, ppid, cmd = m.groups()
        if int(ppid) != 1:
            continue
        if not any(sig in cmd for sig in BROWSER_SIGNATURES):
            continue
        orphans.append((int(pid), cmd[:100]))
    return orphans


def reap_once() -> int:
    orphans = find_orphaned_pids()
    if not orphans:
        return 0
    for pid, cmd in orphans:
        print(f"[reap] pid={pid}  {cmd}", file=sys.stderr)
        try:
            os.kill(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
    return len(orphans)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=30,
                    help="Seconds between sweeps (default: 30)")
    ap.add_argument("--once", action="store_true",
                    help="Reap once and exit (for CI/tests)")
    args = ap.parse_args()

    if args.once:
        n = reap_once()
        print(f"reaped {n}", file=sys.stderr)
        return 0

    print(f"browser_reaper started (interval={args.interval}s)", file=sys.stderr)
    while True:
        try:
            n = reap_once()
            if n:
                print(f"[reap] killed {n} orphaned browser process(es)",
                      file=sys.stderr)
        except Exception as exc:  # noqa: BLE001
            print(f"[reap] sweep failed: {exc}", file=sys.stderr)
        time.sleep(args.interval)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
