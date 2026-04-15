# Benchmark Skills

Claude Code skills (slash commands) for working with the Odoo browser agent benchmark.

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| [create-benchmark-task](create-benchmark-task.md) | `/create-benchmark-task module.task_name` | Create a new hard benchmark task with all required files |
| [write-oracle-solution](write-oracle-solution.md) | `/write-oracle-solution task_name` | Write/fix a Playwright oracle script proving task solvability |
| [validate-benchmark-tasks](validate-benchmark-tasks.md) | `/validate-benchmark-tasks [--all\|--tasks t1,t2]` | Run human + browser-use validation, produce comparison report |

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
