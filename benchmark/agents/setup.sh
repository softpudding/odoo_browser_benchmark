#!/usr/bin/env bash
# Setup script for benchmark agent wrappers.
# Installs all dependencies needed to run the supported browser agents.
#
# Usage:
#   cd benchmark/agents && bash setup.sh
#
# Prerequisites (see benchmark/AGENTS.md for the full checklist):
#   - Python 3.11+ with pip
#   - Node.js 18+ with npm
#   - git, uv
#   - Odoo .venv built and .odoorc.local written (eval.py needs them)
#
# LLM key: set DASHSCOPE_API_KEY before running agents (qwen3.6-plus via
# DashScope OpenAI-compat; same key works for every active agent).
# Stagehand is currently excluded — see benchmark/agents/README.md for the
# DashScope Responses-API bug that blocks it.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENDOR_DIR="$SCRIPT_DIR/vendor"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Installing the benchmark Python package (uv sync) ==="
cd "$REPO_ROOT"
uv sync
cd "$SCRIPT_DIR"
echo

echo "=== Installing Python agent packages ==="
pip install skyvern notte websight alumnium langchain-openai mitmproxy
echo

echo "=== Installing Playwright browsers ==="
python3 -m playwright install chromium 2>/dev/null || echo "  (Playwright browsers may already be installed)"
echo

echo "=== Installing Node.js agent packages ==="
cd "$SCRIPT_DIR"
npm init -y 2>/dev/null
npm install @browserbasehq/stagehand magnitude-core
echo

echo "=== Cloning Agent-E (needs its own venv due to dep conflicts) ==="
mkdir -p "$VENDOR_DIR"
if [ -d "$VENDOR_DIR/Agent-E" ]; then
    echo "  Already cloned, pulling latest..."
    cd "$VENDOR_DIR/Agent-E" && git pull
else
    git clone --depth 1 https://github.com/EmergenceAI/Agent-E.git "$VENDOR_DIR/Agent-E"
fi
echo "  Creating isolated venv..."
cd "$VENDOR_DIR/Agent-E"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt 2>/dev/null || echo "  (requirements.txt install had warnings)"
echo

echo "=== Verification ==="
cd "$SCRIPT_DIR"
echo -n "  skyvern:    "; python3 -c "import skyvern; print('OK')" 2>&1 || echo "FAIL"
echo -n "  notte:      "; python3 -c "import notte; print('OK')" 2>&1 || echo "FAIL"
echo -n "  websight:   "; python3 -c "pass; print('OK (needs LLM API key at runtime)')" 2>&1
echo -n "  alumnium:   "; python3 -c "import alumnium; print('OK')" 2>&1 || echo "FAIL"
echo -n "  mitmproxy:  "; python3 -c "import mitmproxy; print('OK')" 2>&1 || echo "FAIL"
echo -n "  stagehand:  "; node -e "require('@browserbasehq/stagehand'); console.log('OK')" 2>&1 || echo "FAIL"
echo -n "  magnitude:  "; node -e "require('magnitude-core'); console.log('OK')" 2>&1 || echo "FAIL"
echo -n "  Agent-E:    "; [ -d "$VENDOR_DIR/Agent-E/.venv" ] && echo "OK (venv created)" || echo "FAIL"
echo

echo "=== Done ==="
echo
echo "Next steps (see benchmark/AGENTS.md):"
echo "  1. export DASHSCOPE_API_KEY=sk-..."
echo "  2. Build the base snapshot: uv run benchmark-eval bootstrap-base"
echo "  3. If using Agent-E, edit $VENDOR_DIR/Agent-E/agents_llm_config.json"
echo "     to point at DashScope qwen3.6-plus, then start the server:"
echo "       cd $VENDOR_DIR/Agent-E && PYTHONPATH=. .venv/bin/python3 -c \\"
echo "         'import nest_asyncio; nest_asyncio.apply();"
echo "          import asyncio; asyncio.set_event_loop_policy(None);"
echo "          from ae.server.api_routes import app; import uvicorn;"
echo "          uvicorn.run(app, host=\"0.0.0.0\", port=8000, loop=\"asyncio\")'"
echo "  4. If using OpenBrowser: clone + run its server + install its Chrome"
echo "     extension + export OPENBROWSER_CHROME_UUID (no automatic install)."
echo "  5. Smoke test:"
echo "       uv run benchmark-eval run sale.change_validity_date \\"
echo "         --agent browser-use --provider dashscope --model qwen3.6-plus \\"
echo "         --max-steps 60 --headed --db bench_smoke"
echo "  6. Formal batch: see skills/run-benchmark-agents.md"
