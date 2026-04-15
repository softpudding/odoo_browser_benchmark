---
name: benchmark-human-qa
description: Run a reproducible human-vs-browser-use QA sample over 10% of benchmark tasks. Selects a random task subset, shows the human the exact prompt browser-use sees, runs browser-use in parallel, compares artifacts, and adjudicates human failures versus task-design failures. Use when collecting solvability/QA evidence for paper/browser_agent_eval or release curation.
user-invocable: true
argument-hint: [sample-label or seed]
---

# Benchmark Human QA Sample

Use this skill to verify that benchmark tasks are actually solvable by a human,
not just authored to make browser agents fail.

This is a QA workflow for `paper/browser_agent_eval`, so treat it as evidence
collection. Every run must leave behind a reproducible sample manifest and
per-task adjudication artifacts.

## Defaults

- Sample fraction: `10%` of all tasks
- Sample size rule: `ceil(task_count * 0.10)`, minimum `1`
- Sampling method: pseudorandom with a recorded seed
- Default seed when none is given: local date in `YYYYMMDD`
- Default report root:
  `benchmark/reports/human_eval/<sample_label_or_date>/`

## Required artifacts

Create and keep these artifacts:

- `sample_manifest.json`: selected tasks, fraction, seed, total task count
- For each task:
  - `human/`: output of `benchmark/eval.py run --agent human`
  - `browser_use/`: output of `benchmark/eval.py run --agent browser-use`
  - `comparison.json`: machine summary of both runs
  - `adjudication.md`: short note explaining whether the task is human-solvable,
    a task-design bug was fixed, or the human made an execution mistake
- `SUMMARY.md`: running sample-level summary for the paper appendix / QA notes

## Step 1: Select the 10% sample

Use the bundled sampler:

```bash
python .claude/skills/benchmark-human-qa/scripts/sample_tasks.py \
  --tasks-root benchmark/tasks \
  --fraction 0.10 \
  --seed <seed> \
  --output benchmark/reports/human_eval/<sample>/sample_manifest.json
```

Rules:

- Always record the seed.
- Do not hand-pick or reshuffle the sampled tasks unless a task directory is
  broken or intentionally excluded; if you exclude one, document why.
- Reuse the same manifest for the whole QA pass.

## Step 2: For each sampled task, run human and browser-use in parallel

For each task in the manifest:

1. Start the `browser-use` run first in a separate terminal session and give it
   a dedicated output directory:

```bash
PYTHONPATH=. python benchmark/eval.py run <task_id> \
  --agent browser-use \
  --output-dir benchmark/reports/human_eval/<sample>/<task_id>/browser_use
```

2. Build the exact prompt that browser-use sees:

```bash
python .claude/skills/benchmark-human-qa/scripts/build_exact_prompt.py <task_id> \
  --base-url <base_url> \
  --db <db_name> \
  --login <login> \
  --password <password>
```

3. Show that prompt to the human verbatim. Do not paraphrase. The human must
   see the same instruction block the agent sees, including:
   - base URL
   - start URL
   - database-selection instruction
   - login/password instruction
   - the exact task text

4. Run the human episode and save artifacts separately:

```bash
PYTHONPATH=. python benchmark/eval.py run <task_id> \
  --agent human \
  --output-dir benchmark/reports/human_eval/<sample>/<task_id>/human
```

5. Wait for both runs to finish before adjudicating.

Important:

- Keep both runs isolated. Do not make the human and browser-use share a live
  browser tab.
- Prefer the auto-isolated default in `benchmark/eval.py`; do not force
  `--no-isolate` unless debugging.
- If the browser-use run dies for infrastructure reasons (credits, API outage,
  interpreter issue), document that as infra failure, not task failure.

## Step 3: Compare the two runs

Use the bundled comparison helper:

```bash
python .claude/skills/benchmark-human-qa/scripts/compare_runs.py \
  benchmark/reports/human_eval/<sample>/<task_id>/human \
  benchmark/reports/human_eval/<sample>/<task_id>/browser_use \
  --output benchmark/reports/human_eval/<sample>/<task_id>/comparison.json
```

Then inspect:

- `score.json`
- `postcondition_failures.json`
- `state_diff.json`
- `agent_result.json`
- task files:
  `prompt.md`, `seed.py`, `check.py`, `expected_state.json`, `state_spec.yaml`

## Step 4: Adjudicate human failure correctly

If the human passes, mark the task as human-solvable and continue.

If the human fails, classify the failure before moving on:

### A. Task-design failure

Fix the task if the failure came from:

- ambiguous prompt wording
- missing entity identifiers
- prompt/seed mismatch
- hidden prerequisite not established by `seed.py`
- impossible or misleading UI instructions
- bad oracle / `expected_state.json` mismatch
- incorrect or over-strict `check.py`
- insufficient timeout for a reasonable human

When you fix a task-design problem:

- patch the task files
- rerun the same task for human and browser-use
- replace the prior adjudication with the fixed result
- document the fix in `adjudication.md`

Do not weaken the task just to make it pass. Only fix real design defects.

### B. Human execution error

Do not change the task if the failure was caused by the human deviating from the
prompt, for example:

- edited the wrong record
- skipped a required confirmation/save
- entered the wrong literal value
- ignored a rule in the prompt
- stopped before the workflow actually completed

In this case:

- explain exactly where the human diverged from the prompt or expected state
- record it in `adjudication.md`
- count the task as human-failed-by-execution, not task-invalid
- continue to the next sampled task

## Step 5: Maintain paper-grade QA notes

`SUMMARY.md` should track one line per sampled task with:

- task id
- human result
- browser-use result
- adjudication label:
  `human_pass`, `task_bug_fixed`, `human_error`, `infra_failure`
- short cause note

This summary is the source material for:

- sampled solvability evidence
- adjudication logs
- dual-review / annotation-QA appendix notes in `paper/browser_agent_eval`

## Guardrails

- Never paraphrase the task when presenting it to the human if exact-prompt
  parity is the point of the run.
- Never decide “human cannot do this” from the self-reported yes/no alone;
  inspect the artifacts and postconditions.
- Never silently discard sampled tasks because they are inconvenient.
- Never patch validator logic without checking whether the run artifacts show a
  real oracle bug.
- If the task itself is broken, fix it immediately before continuing the sample.

## Quick start

```bash
python .claude/skills/benchmark-human-qa/scripts/sample_tasks.py \
  --seed 20260415 \
  --output benchmark/reports/human_eval/20260415_sample/sample_manifest.json
```

Then iterate the selected tasks using the workflow above.
