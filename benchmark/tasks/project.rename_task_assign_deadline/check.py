"""Postcondition checks for project.rename_task_assign_deadline."""

from datetime import date


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", "Operations Knowledge Base")],
        limit=1,
    )
    if not project:
        return ["Project 'Operations Knowledge Base' not found"]

    old_name = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Draft launch checklist"),
    ], limit=1)
    if old_name:
        failures.append("Old task name 'Draft launch checklist' should no longer exist")

    tasks = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Draft launch checklist follow-up"),
    ])
    if len(tasks) != 1:
        failures.append(
            f"Expected exactly 1 renamed task, found {len(tasks)}"
        )
        return failures

    task = tasks[0]
    if task.stage_id.name != "In Progress":
        failures.append(
            f"Renamed task stage is '{task.stage_id.name}', expected 'In Progress'"
        )
    if str(task.date_deadline) != "2026-05-26 16:00:00":
        failures.append(
            f"Renamed task deadline is {task.date_deadline}, expected 2026-05-27"
        )

    distractor = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Review mobile checklist"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor task 'Review mobile checklist' not found")
    else:
        if distractor.stage_id.name != "To Do":
            failures.append(
                f"Distractor task stage is '{distractor.stage_id.name}', expected 'To Do'"
            )
        if distractor.date_deadline:
            failures.append("Distractor task should not have a deadline")
        if distractor.user_ids:
            failures.append("Distractor task should not have assignees")

    return failures
