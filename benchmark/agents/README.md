# Benchmark Agent Wrappers

Thin wrapper scripts that adapt third-party browser agents to the benchmark
`eval.py --agent command` interface. Each agent receives a natural-language
task and a URL, navigates the Odoo UI autonomously, and the benchmark scores
the resulting database state.

## Quick start

```bash
# Install all dependencies
cd benchmark/agents && bash setup.sh

# Run a task with any agent
uv run benchmark-eval run <task> --agent command \
    --cmd "python benchmark/agents/run_<agent>.py"
```

## Environment variables (set automatically by eval.py)

| Variable | Description |
|---|---|
| `BENCHMARK_INSTRUCTION` | Natural-language task for the agent |
| `BENCHMARK_START_URL` | Full URL the agent should open first |
| `BENCHMARK_BASE_URL` | Odoo base URL (e.g. `http://127.0.0.1:8069`) |
| `BENCHMARK_DB` | Database name |
| `BENCHMARK_LOGIN` | Login credential |
| `BENCHMARK_PASSWORD` | Password credential |
| `BENCHMARK_MAX_STEPS` | Maximum agent steps |

## Supported agents

### Fully working (tested with DashScope/qwen3.6-plus)

| Agent | Wrapper | Language | Install | Run command |
|-------|---------|----------|---------|-------------|
| [Notte](https://github.com/nottelabs/notte) | `run_notte.py` | Python | `pip install notte` | `python benchmark/agents/run_notte.py` |
| [Skyvern](https://github.com/skyvern-ai/skyvern) | `run_skyvern.py` | Python | `pip install skyvern` | `python benchmark/agents/run_skyvern.py` |
| [WebSight](https://github.com/SuperAce100/websight) | `run_websight.py` | Python | `pip install websight` | `python benchmark/agents/run_websight.py` |
| [Alumnium](https://github.com/alumnium-hq/alumnium) | `run_alumnium.py` | Python | `pip install alumnium` | `python benchmark/agents/run_alumnium.py` |

### Require external setup

| Agent | Wrapper | Requirement | Run command |
|-------|---------|-------------|-------------|
| [Agent-E](https://github.com/EmergenceAI/Agent-E) | `run_agent_e.py` | Separate server in own venv (see wrapper header) | `python benchmark/agents/run_agent_e.py` |
| [OpenBrowser](https://github.com/softpudding/OpenBrowser) | `run_openbrowser.py` | Server + Chrome extension + `OPENBROWSER_CHROME_UUID` | `python benchmark/agents/run_openbrowser.py` |

### Require specific API keys (not DashScope-compatible)

| Agent | Wrapper | Requirement | Run command |
|-------|---------|-------------|-------------|
| [Stagehand](https://github.com/browserbase/stagehand) | `run_stagehand.mjs` | `OPENAI_API_KEY` (hardcodes gpt-4.1-mini) | `node benchmark/agents/run_stagehand.mjs` |
| [Magnitude](https://github.com/magnitudedev/browser-agent) | `run_magnitude.mjs` | `ANTHROPIC_API_KEY` (BAML-locked) | `node benchmark/agents/run_magnitude.mjs` |

### Evaluated but excluded

| Agent | Reason |
|-------|--------|
| [Browserable](https://github.com/browserable/browserable) | Requires external browser-as-a-service (Hyperbrowser/Steel) |
| [Agent-S](https://github.com/simular-ai/agent-s) | Desktop GUI agent (PyAutoGUI), not a browser agent |
| [AgentOccam](https://github.com/amazon-science/AgentOccam) | Dead research artifact (3 commits), no usable API |

## LLM configuration

All wrappers use `_env_setup.py` to auto-detect LLM credentials:

1. `OPENAI_API_KEY` — used directly if set
2. `DASHSCOPE_API_KEY` — mapped to OpenAI-compatible endpoint automatically
3. `BAILIAN_API_KEY` — same as DashScope

Set `BENCHMARK_MODEL` to override the default model (default: `qwen3.6-plus`).

## Test results (contacts.update_contact_phone, qwen3.6-plus)

| Agent | Status | F1 | Wall Clock | API Calls | Writes |
|-------|--------|----|-----------|-----------|--------|
| Notte | **PASS** | 1.0 | 128.7s | 22 | 9 |
| Agent-E | **PASS** | 1.0 | 240s | 23 | 9 |
| OpenBrowser | **PASS** | 1.0 | 240s | 28 | 13 |
| Skyvern | Connected | 0.0 | 240s | 18 | 6 |
| Alumnium | Connected | 0.0 | 110s | 6 | 2 |
| WebSight | Connected | 0.0 | 240s | 3 | 1 |
