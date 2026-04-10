# Browser Use With Local Odoo

Odoo already ships deterministic browser coverage through `HttpCase.start_tour(...)`.
This helper is for exploratory or natural-language smoke testing against a running local instance, using a local Browser Use browser instead of Browser Use Cloud.

## When this is useful

- Reproduce a UI issue quickly with natural-language instructions.
- Run one-off smoke checks on a local module or branch.
- Drive a local Chromium or a real local Chrome window without exposing `localhost`.

## Files

- `setup/browser_use_local.py`: Python helper built on `browser_use.Agent`, local browser sessions, and pluggable LLM backends.

## Requirements

1. Run a local Odoo server, for example on `http://127.0.0.1:8069`.
2. Use a Python interpreter where the `browser_use` package is installed.
3. Configure the model key for the provider you want to use.

Agent tasks still need model credentials even in local-browser mode.

## Basic usage

Use the default Browser Use cloud-model backend:

```bash
python3 setup/browser_use_local.py \
  "Log in as admin and verify the CRM pipeline loads without console errors." \
  --provider browser-use \
  --login admin \
  --password admin
```

Use Alibaba Cloud Bailian / DashScope in OpenAI-compatible mode. The helper now defaults to `qwen-vl-max`, which is a better fit for Browser Use than `glm-5` in practice:

```bash
export DASHSCOPE_API_KEY=your_key
python3 setup/browser_use_local.py \
  "Open Sales and create a quotation draft for Azure Interior." \
  --provider dashscope \
  --login admin \
  --password admin
```

If you want Browser Use to drive a real local Chrome window instead:

```bash
python3 setup/browser_use_local.py \
  "Open Settings and inspect the users list." \
  --browser real \
  --headed \
  --provider dashscope \
  --db my_odoo_db \
  --login admin \
  --password admin
```

## Profiles

To inspect the local profiles visible to `browser-use` in real-browser mode:

```bash
python3 setup/browser_use_local.py --browser real --list-profiles
```

You can then pass one with `--profile PROFILE_NAME`.

## Provider Notes

- `--provider browser-use`: uses `BROWSER_USE_API_KEY` and Browser Use's own hosted model endpoint.
- `--provider dashscope`: uses `DASHSCOPE_API_KEY` or `BAILIAN_API_KEY`, defaults to `https://dashscope.aliyuncs.com/compatible-mode/v1`, and defaults to `qwen-vl-max`.
- `glm-5` is still available with `--model glm-5`, but Browser Use tends to be less stable with it unless you build a custom non-thinking wrapper for DashScope structured output.
- `--provider openai-compatible`: uses `OPENAI_API_KEY` by default and lets you override `--llm-base-url` for any OpenAI-compatible endpoint.

## Notes

- Credentials passed on the command line may end up in shell history, process lists, and Browser Use logs.
- API keys are expected in environment variables and are not written into this repo.
- This helper stays fully local on the browser side, but the model call still needs the relevant LLM/API credentials.
- This helper is best for ad hoc checks. Repeatable regressions should still graduate into regular Odoo tests or tours.

## Agent Eval

If you install the `agent_eval` addon, the helper can wrap a run in an
evaluation session and print the final diff/evaluation report:

```bash
python3 setup/browser_use_local.py \
  "Open CRM and update the partner phone number." \
  --provider dashscope \
  --db my_odoo_db \
  --login admin \
  --password admin \
  --eval-spec-file /path/to/spec.json
```

`--eval-spec-file` currently requires `--db`, `--login`, and `--password`
because the helper starts and finalizes the evaluation session over XML-RPC.

See `doc/agent_eval.md` for the spec format.

To use a built-in case prepared server-side instead of writing a spec file:

```bash
python3 setup/browser_use_local.py \
  --provider dashscope \
  --db my_odoo_db \
  --login admin \
  --password admin \
  --eval-case crm_forecast_drag_and_win
```

The server-side case preparation step resets the task-scoped database records and
seeds the expected starting state before the eval session begins.

To list the built-in cases available on the server:

```bash
python3 setup/browser_use_local.py \
  --db my_odoo_db \
  --login admin \
  --password admin \
  --list-eval-cases
```
