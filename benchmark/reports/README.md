# Ledger evaluation records

This directory preserves development checks, oracle verification, and agent
evaluation artifacts. The published paper defines the experimental comparisons;
the presence of a run here does not make it a paper baseline.

- `formal_run/` contains agent outputs and append-only scheduling queues. Queues
  include claims, retries, and completed attempts; counting queue rows is not the
  same as counting unique evaluated tasks.
- `human_eval/` contains a small set of author-operated quality-assurance
  walkthroughs and debugging attempts. These are not a recruited-participant
  study or a human-performance baseline.
- Other subdirectories contain development and validation runs, which may use
  different task versions, providers, models, or budgets.

For the camera-ready code release, local home-directory prefixes, machine
hostnames, and worker identifiers in the tracked text reports were replaced
with consistent generic identifiers, including dispatcher log filenames. Synthetic POS access tokens in trace
argument summaries were redacted. Task definitions, score values, operation
names, timestamps, and queue row counts were preserved. Paths recorded inside
old outputs describe their original execution context and may not resolve on a
new machine.

This cleanup applies to the release tree. Earlier Git commits retain their
historical contents.
