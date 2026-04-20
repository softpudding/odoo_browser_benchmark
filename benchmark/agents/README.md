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

### Require specific API keys

| Agent | Wrapper | Requirement | Run command |
|-------|---------|-------------|-------------|
| [Stagehand](https://github.com/browserbase/stagehand) | `run_stagehand.mjs` | `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`. Auto-detects Anthropic. But v2 hardcodes `gpt-4.1-mini` internally — ignores custom `modelName`. | `node benchmark/agents/run_stagehand.mjs` |
| [Magnitude](https://github.com/magnitudedev/browser-agent) | `run_magnitude.mjs` | `ANTHROPIC_API_KEY`. BAML runtime error (`CreatePartialRecipe` undefined) — framework-level bug, not an API key issue. | `node benchmark/agents/run_magnitude.mjs` |

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

## Test results (qwen3.6-plus)

### Easy: contacts.update_contact_phone (change one field)

| Agent | F1 | Wall Clock | API Calls | Writes |
|-------|----|-----------|-----------|--------|
| Notte | **1.0** | 128.7s | 22 | 9 |
| Agent-E | **1.0** | 240s | 23 | 9 |
| OpenBrowser | **1.0** | 240s | 28 | 13 |
| Skyvern | 0.0 | 240s | 18 | 6 |
| Alumnium | 0.0 | 110s | 6 | 2 |
| WebSight | 0.0 | 240s | 3 | 1 |

### Medium: crm.mark_opportunity_won_update_revenue (set revenue, priority, mark won)

| Agent | F1 | Wall Clock | API Calls | Writes | Notes |
|-------|----|-----------|-----------|--------|-------|
| Agent-E | 0.0 | 194s | 33 | 17 | 3/4 edits correct (revenue, won, probability). Only missed priority (1 vs 2 stars) |
| Skyvern | 0.0 | 300s | 36 | 14 | Connected, navigated CRM |
| OpenBrowser | 0.0 | 300s | 12 | 2 | Connected, navigated |
| Alumnium | 0.0 | 29s | 6 | 1 | Minimal interaction |
| WebSight | 0.0 | 300s | 5 | 1 | Minimal interaction |
| Notte | 0.0 | 7s | 1 | 0 | Crashed early |

### Hard: sale_project.confirm_quote_and_update_generated_project (5-step cross-app)

| Agent | F1 | Wall Clock | API Calls | Writes | Notes |
|-------|----|-----------|-----------|--------|-------|
| Agent-E | 0.0 | 420s | 81 | 37 | Confirmed SO (1/4 required ops), closest to completing |
| OpenBrowser | 0.0 | 420s | 26 | 5 | Connected, navigated |
| Skyvern | 0.0 | 420s | 24 | 8 | Connected, navigated |
| WebSight | 0.0 | 420s | 4 | 1 | Minimal interaction |
| Alumnium | 0.0 | 42s | 4 | 1 | Minimal interaction |
| Notte | 0.0 | 7s | 0 | 0 | Crashed early |

## Root cause analysis

Investigation with isolated super-simple tasks ("just log in to Odoo"):

| Agent | Can log in? | Root cause of task failures |
|-------|------------|----------------------------|
| **Agent-E** | Yes | Best performer. AG2 multi-agent framework with Playwright. Slow but methodical. |
| **Notte** | Yes (with local Session) | Crashes on complex tasks due to litellm/model config issues. Works well when it runs. |
| **OpenBrowser** | Yes | Multimodal (screenshot-based). Works but slow; relies on Qwen VL model quality. |
| **Skyvern** | Yes (verified) | Navigates and interacts with Odoo (18 API calls, 6 writes on easy task) but fails to edit specific form fields. Very slow (~90s/step). |
| **Alumnium** | Yes (verified) | Step-level `do()` executes actions at DOM level but qwen3.6-plus can't reliably map NL to Odoo form field edits. Reports success even when field wasn't changed. |
| **WebSight** | No | **Hallucinates execution.** Generates correct plans but claims task is complete on blank screenshots. VLM responses don't follow expected `<reasoning>/<action>` format. |
| **Stagehand** | N/A | Hardcodes `gpt-4.1-mini` internally, ignores all model config. With Anthropic key, still uses OpenAI model. Framework bug. |
| **Magnitude** | N/A | BAML runtime crash (`CreatePartialRecipe` undefined). Framework-level bug unrelated to API keys. |
