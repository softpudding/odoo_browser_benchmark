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

### Fully working

| Agent | Wrapper | Language | Install | API Key | Run command |
|-------|---------|----------|---------|---------|-------------|
| [Notte](https://github.com/nottelabs/notte) | `run_notte.py` | Python | `pip install notte` | DashScope or OpenAI | `python benchmark/agents/run_notte.py` |
| [Skyvern](https://github.com/skyvern-ai/skyvern) | `run_skyvern.py` | Python | `pip install skyvern` | DashScope or OpenAI | `python benchmark/agents/run_skyvern.py` |
| [Alumnium](https://github.com/alumnium-hq/alumnium) | `run_alumnium.py` | Python | `pip install alumnium` | DashScope or OpenAI | `python benchmark/agents/run_alumnium.py` |
| [Magnitude](https://github.com/magnitudedev/browser-agent) | `run_magnitude.mjs` | Node.js | `npm install magnitude-core` | **Anthropic** (or Google/OpenAI) | `node benchmark/agents/run_magnitude.mjs` |

### Require external setup

| Agent | Wrapper | Requirement | Run command |
|-------|---------|-------------|-------------|
| [Agent-E](https://github.com/EmergenceAI/Agent-E) | `run_agent_e.py` | Separate server in own venv (see wrapper header) | `python benchmark/agents/run_agent_e.py` |
| [OpenBrowser](https://github.com/softpudding/OpenBrowser) | `run_openbrowser.py` | Server + Chrome extension + `OPENBROWSER_CHROME_UUID` | `python benchmark/agents/run_openbrowser.py` |

### Partially working (framework limitations)

| Agent | Wrapper | Issue |
|-------|---------|-------|
| [WebSight](https://github.com/SuperAce100/websight) | `run_websight.py` | Hallucinates execution — claims task complete on blank screenshots. VLM response parsing is broken. |
| [Stagehand](https://github.com/browserbase/stagehand) | `run_stagehand.mjs` | v2 hardcodes `gpt-4.1-mini` internally, ignores all `modelName` config. Framework bug. |

### Evaluated but excluded

| Agent | Reason |
|-------|--------|
| [Browserable](https://github.com/browserable/browserable) | Requires external browser-as-a-service (Hyperbrowser/Steel) |
| [Agent-S](https://github.com/simular-ai/agent-s) | Desktop GUI agent (PyAutoGUI), not a browser agent |
| [AgentOccam](https://github.com/amazon-science/AgentOccam) | Dead research artifact (3 commits), no usable API |

## LLM configuration

All Python wrappers use `_env_setup.py` to auto-detect LLM credentials:

1. `OPENAI_API_KEY` — used directly if set
2. `DASHSCOPE_API_KEY` — mapped to OpenAI-compatible endpoint automatically
3. `BAILIAN_API_KEY` — same as DashScope

Node.js wrappers (Magnitude, Stagehand) detect `ANTHROPIC_API_KEY` first,
then fall back to `OPENAI_API_KEY` / `DASHSCOPE_API_KEY`.

Set `BENCHMARK_MODEL` to override the default model (default: `qwen3.6-plus`
for Python agents, `claude-sonnet-4` for Magnitude).

## Test results

### Easy: contacts.update_contact_phone (change one field)

| Agent | LLM | F1 | Wall Clock | API Calls | Writes |
|-------|-----|----|-----------|-----------|--------|
| Magnitude | Claude Sonnet 4 | **1.0** | 102s | 22 | 9 |
| Notte | qwen3.6-plus | **1.0** | 129s | 22 | 9 |
| Agent-E | qwen3.6-plus | **1.0** | 240s | 23 | 9 |
| OpenBrowser | qwen3.6-plus | **1.0** | 240s | 28 | 13 |
| Skyvern | qwen3.6-plus | 0.0 | 240s | 18 | 6 |
| Alumnium | qwen3.6-plus | 0.0 | 110s | 6 | 2 |

### Medium: crm.mark_opportunity_won_update_revenue (set revenue, priority, mark won)

| Agent | LLM | F1 | Wall Clock | API Calls | Writes | Notes |
|-------|-----|----|-----------|-----------|--------|-------|
| Agent-E | qwen3.6-plus | 0.0 | 194s | 33 | 17 | 3/4 edits correct. Only missed priority (1 vs 2 stars) |
| Magnitude | Claude Sonnet 4 | 0.0 | 300s | 142 | 49 | Very active (most API calls) but no edits landed |
| Skyvern | qwen3.6-plus | 0.0 | 300s | 36 | 14 | Connected, navigated CRM |
| OpenBrowser | qwen3.6-plus | 0.0 | 300s | 12 | 2 | Connected, navigated |
| Alumnium | qwen3.6-plus | 0.0 | 29s | 6 | 1 | Minimal interaction |
| Notte | qwen3.6-plus | 0.0 | 7s | 1 | 0 | Crashed early |

### Hard: sale_project.confirm_quote_and_update_generated_project (5-step cross-app)

| Agent | LLM | F1 | Wall Clock | API Calls | Writes | Notes |
|-------|-----|----|-----------|-----------|--------|-------|
| Magnitude | Claude Sonnet 4 | 0.0 | 420s | 142 | 49 | Confirmed SO (1/4 ops). 1/2 edits matched. |
| Agent-E | qwen3.6-plus | 0.0 | 420s | 81 | 37 | Confirmed SO (1/4 required ops) |
| OpenBrowser | qwen3.6-plus | 0.0 | 420s | 26 | 5 | Connected, navigated |
| Skyvern | qwen3.6-plus | 0.0 | 420s | 24 | 8 | Connected, navigated |
| Alumnium | qwen3.6-plus | 0.0 | 42s | 4 | 1 | Minimal interaction |
| Notte | qwen3.6-plus | 0.0 | 7s | 0 | 0 | Crashed early |

## Root cause analysis

Investigation with isolated super-simple tasks ("just log in to Odoo"):

| Agent | Can log in? | Root cause of task failures |
|-------|------------|----------------------------|
| **Magnitude** | Yes | Works well with Claude Sonnet 4. Uses BAML + Patchright. Needs `ANTHROPIC_API_KEY`. |
| **Agent-E** | Yes | Best performer on complex tasks. AG2 multi-agent framework. Slow but methodical. |
| **Notte** | Yes | Good on easy tasks but crashes on complex ones (litellm/model config issues). |
| **OpenBrowser** | Yes | Multimodal (screenshot-based). Works but slow; tied to Chrome extension. |
| **Skyvern** | Yes | Navigates Odoo (18+ API calls) but can't reliably edit specific form fields. ~90s/step. |
| **Alumnium** | Yes | DOM-level `do()` works for login but qwen3.6-plus can't map NL to Odoo form edits. Silently claims success. |
| **WebSight** | No | Hallucinates — claims task complete on blank screenshots. Broken VLM response parsing. |
| **Stagehand** | N/A | Hardcodes `gpt-4.1-mini`, ignores all model config including Anthropic. Framework bug. |

## Troubleshooting

### Playwright/Patchright browser not found

Agents use different Playwright versions. If you see "Executable doesn't exist":
```bash
# For Python agents (skyvern, notte, alumnium, websight)
python3 -m playwright install chromium

# For Node.js agents (magnitude, stagehand)
npx playwright install chromium
```

### DashScope `json_object` errors

DashScope requires "json" in the prompt when using `response_format=json_object`.
Alumnium's wrapper patches `with_structured_output` to use `method="function_calling"` instead.

### DashScope thinking mode conflicts

`qwen3.6-plus` enables thinking mode by default, which rejects `tool_choice=required`.
Alumnium's wrapper adds `enable_thinking: False` to the model kwargs.

### Agent-E async event loop crash

Agent-E's AG2 framework calls `loop.run_until_complete()` inside uvicorn's async loop.
Fix: start with `nest_asyncio` and force `asyncio` loop (not uvloop):
```bash
PYTHONPATH=. .venv/bin/python3 -c "
    import nest_asyncio; nest_asyncio.apply()
    import asyncio; asyncio.set_event_loop_policy(None)
    from ae.server.api_routes import app
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, loop='asyncio')
"
```

### Agent-E dependency conflicts

Agent-E pins `pydantic==2.6.2` which breaks notte/alumnium/skyvern (need 2.11+).
Always install Agent-E in its own venv:
```bash
cd Agent-E && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

### Magnitude BAML `CreatePartialRecipe` error

This happens when `new Agent()` is created without an `llm` config — it defaults
to Google AI with a missing API key. Pass explicit LLM config:
```javascript
const agent = new Agent({
  llm: {
    provider: "anthropic",
    options: { model: "claude-sonnet-4-20250514", apiKey: process.env.ANTHROPIC_API_KEY }
  },
  connectors: [new BrowserConnector({ url: startUrl })]
});
```

### DB name too long

Tasks with long names (e.g. `sale_project.confirm_quote_and_update_generated_project`)
exceed PostgreSQL's 63-char limit for auto-generated DB names. Use `--db <short_name>`:
```bash
uv run benchmark-eval run <long_task_name> --agent command --cmd "..." --db bench_short
```

### Environment variables not reaching subprocesses

`uv run` creates an isolated env. Pass API keys explicitly in `--cmd`:
```bash
--cmd "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY node benchmark/agents/run_magnitude.mjs"
```
