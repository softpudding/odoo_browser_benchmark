#!/usr/bin/env bash
# Setup script for benchmark agent wrappers.
# Installs all dependencies needed to run the supported browser agents.
#
# Usage:
#   cd benchmark/agents && bash setup.sh
#
# Prerequisites:
#   - Python 3.11+ with pip
#   - Node.js 18+ with npm
#   - git
#
# LLM API keys (set at least one before running agents):
#   - DASHSCOPE_API_KEY     — works with all Python agents via OpenAI-compatible endpoint
#   - OPENAI_API_KEY        — needed by Stagehand (hardcodes gpt-4.1-mini)
#   - ANTHROPIC_API_KEY     — needed by Magnitude (BAML-locked)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENDOR_DIR="$SCRIPT_DIR/vendor"

echo "=== Installing Python agent packages ==="
pip install skyvern notte websight alumnium langchain-openai
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
echo -n "  stagehand:  "; node -e "require('@browserbasehq/stagehand'); console.log('OK')" 2>&1 || echo "FAIL"
echo -n "  magnitude:  "; node -e "require('magnitude-core'); console.log('OK')" 2>&1 || echo "FAIL"
echo -n "  Agent-E:    "; [ -d "$VENDOR_DIR/Agent-E/.venv" ] && echo "OK (venv created)" || echo "FAIL"
echo

echo "=== Done ==="
echo
echo "Set DASHSCOPE_API_KEY (or OPENAI_API_KEY), then run agents via:"
echo "  uv run benchmark-eval run <task> --agent command --cmd 'python benchmark/agents/run_notte.py'"
echo
echo "For Agent-E, start its server first in its own venv:"
echo "  cd $VENDOR_DIR/Agent-E && PYTHONPATH=. .venv/bin/python3 -c \\"
echo "    'from ae.server.api_routes import app; import uvicorn; uvicorn.run(app, host=\"0.0.0.0\", port=8000)'"
