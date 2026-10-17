# Ledger browser-agent wrappers

These adapters connect third-party browser agents to `benchmark-eval run
--agent command`. The harness supplies a task instruction, start URL, and
synthetic login; it scores the resulting database state and operation trace.
See the [repository README](../../README.md) for Odoo and dataset setup.

## Available adapters

| Agent | Runner | Additional setup |
| --- | --- | --- |
| browser-use | `--agent browser-use` | Install `browser-use` in the repository `.venv` |
| Notte | `python benchmark/agents/run_notte.py` | `notte` |
| Skyvern | `python benchmark/agents/run_skyvern.py` | `skyvern` |
| Alumnium | `python benchmark/agents/run_alumnium.py` | `alumnium`, `langchain-openai` |
| Magnitude | `node benchmark/agents/run_magnitude.mjs` | `magnitude-core` |
| Stagehand | `node benchmark/agents/run_stagehand.mjs` | `@browserbasehq/stagehand` |
| WebSight | `python benchmark/agents/run_websight.py` | `websight` |
| Agent-E | `python benchmark/agents/run_agent_e.py` | Agent-E server in its own virtual environment |
| OpenBrowser | `python benchmark/agents/run_openbrowser.py` | Server, Chrome extension, `OPENBROWSER_CHROME_UUID` |

Stagehand and WebSight are included in the archived formal-run records, each
with completed entries covering 424 distinct tasks. Inclusion means the adapter
was evaluated; it does not mean every task succeeded. The old development
labels “blocked”, “partially working”, and “excluded from current runs” do not
describe the released evaluation coverage. Use the paper for the definition of
its reported comparison set, and [reports/README.md](../reports/README.md) for
the scope of historical runs and retries.

## Installation and execution

`setup.sh` installs the external Python/Node packages and creates an isolated
Agent-E environment. Run it with the Python environment intended for those
agents active:

```bash
(cd benchmark/agents && bash setup.sh)
```

For a single Python wrapper, invoke the interpreter in which that agent is
installed. For example:

```bash
uv run benchmark-eval run sale.change_validity_date --agent command \
  --cmd "/absolute/path/to/agent-venv/bin/python benchmark/agents/run_notte.py" \
  --output-dir /tmp/ledger-notte
```

Node adapters use `node` in place of the Python interpreter. Agent-E and
OpenBrowser require their separate services; see [benchmark/AGENTS.md](../AGENTS.md).
Third-party packages installed by `setup.sh` are not all pinned by `uv.lock`.
Record their installed versions when reproducing an experiment.

## Models and credentials

Python wrappers use `_env_setup.py`: an explicit `OPENAI_API_KEY` takes
precedence over `DASHSCOPE_API_KEY` or `BAILIAN_API_KEY`. Set the corresponding
base URL and `BENCHMARK_MODEL` for the intended provider. Avoid leaving an
unrelated provider's key/base URL set in the same environment.

The released formal runner uses **OpenAI `gpt-4.1-mini` for Stagehand**. Earlier
Qwen/DashScope Responses API trials encountered a multi-turn serialization
error; that was a provider-specific development failure, not an exclusion of
Stagehand from the released run. Reproduce its provider configuration explicitly:

```bash
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_BASE_URL=https://api.openai.com/v1
export BENCHMARK_MODEL=gpt-4.1-mini
uv run benchmark-eval run sale.change_validity_date --agent command \
  --cmd "node benchmark/agents/run_stagehand.mjs" \
  --max-steps 60 --output-dir /tmp/ledger-stagehand
```

WebSight's wrapper includes routing and action-call compatibility fixes used by
the archived runs. Its early smoke-test observations should not be used as a
blanket current compatibility claim.

Magnitude can select Anthropic, OpenAI-compatible/DashScope, or Google
credentials. With an Anthropic key present it prefers Anthropic by default;
`BENCHMARK_PROVIDER` and `BENCHMARK_MODEL` control the choice. Historical
Magnitude runs include different provider/model configurations, so consult the
specific run's metadata before combining results.

## Harness-provided environment

| Variable | Meaning |
| --- | --- |
| `BENCHMARK_INSTRUCTION` | Natural-language task |
| `BENCHMARK_START_URL` | Initial URL |
| `BENCHMARK_BASE_URL` | Per-episode Odoo URL |
| `BENCHMARK_DB` | Episode database |
| `BENCHMARK_LOGIN`, `BENCHMARK_PASSWORD` | Synthetic Odoo credentials |
| `BENCHMARK_MAX_STEPS` | Agent step limit |

## Troubleshooting

- **Browser executable missing:** install Chromium with the same Python or Node
  Playwright version used by that wrapper (`python -m playwright install
  chromium` or `npx playwright install chromium`).
- **Python module missing:** select the interpreter where that package was
  installed. The Odoo `.venv` and external agent environments may differ.
- **Agent-E dependency or event-loop errors:** keep its dependencies in its own
  environment and follow the server startup instructions in `benchmark/AGENTS.md`.
- **Stagehand provider errors:** verify the explicit model, key, and base URL
  above; the direct wrapper otherwise defaults to a Qwen-compatible setup.
- **A task is claimed complete but receives a failure score:** inspect
  `score.json`, database differences, and operation traces. An agent's own
  completion message is not the ground-truth verdict.
