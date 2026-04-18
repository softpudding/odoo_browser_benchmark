# Benchmark Skills

Claude Code skills (slash commands) for working with the Odoo browser agent benchmark.

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| [create-benchmark-task](create-benchmark-task.md) | `/create-benchmark-task module.task_name` | Create a new hard benchmark task with all required files |
| [expand-benchmark-coverage](expand-benchmark-coverage.md) | `/expand-benchmark-coverage [module]` | Identify under-covered Odoo modules and propose new task ideas |
| [write-oracle-solution](write-oracle-solution.md) | `/write-oracle-solution task_name` | Write/fix a Playwright oracle script proving task solvability |
| [validate-benchmark-tasks](validate-benchmark-tasks.md) | `/validate-benchmark-tasks [--all\|--tasks t1,t2]` | Run human + browser-use validation, produce comparison report |
| [relentless-benchmark-pool](relentless-benchmark-pool.md) | `/relentless-benchmark-pool [N:stop]` | Sustained rolling pool of N parallel builders with optimizations from prior batches |

## Setup

These skills are installed in `.claude/skills/`. To use them, ensure
each skill directory under `.claude/skills/<name>/SKILL.md` exists.

The canonical copies live here in `skills/`. To sync after editing:

```bash
for f in skills/*.md; do
  name=$(basename "$f" .md)
  mkdir -p .claude/skills/$name
  cp "$f" .claude/skills/$name/SKILL.md
done
```
