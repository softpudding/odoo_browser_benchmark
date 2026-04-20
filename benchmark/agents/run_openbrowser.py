#!/usr/bin/env python3
"""Benchmark wrapper for OpenBrowser (https://github.com/softpudding/OpenBrowser).

*** NOT VIABLE FOR AUTOMATED BENCHMARKING ***

OpenBrowser requires:
1. A running server (python main.py on port 8765)
2. Chrome with the OpenBrowser extension installed
3. A WebSocket connection from the extension to the server
4. A chrome_uuid token from the connected browser

This architecture makes it impossible to run in an automated benchmark
pipeline — it cannot launch its own browser or operate headlessly.

The wrapper is kept here for documentation purposes only.
"""

import sys

def main():
    print(
        "OpenBrowser is not compatible with automated benchmarking.\n"
        "It requires a Chrome extension connected via WebSocket.\n"
        "See run_openbrowser.py header for details.",
        file=sys.stderr,
    )
    sys.exit(1)

if __name__ == "__main__":
    main()
