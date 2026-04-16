"""Postcondition checks for project.duplicate_task_assign_deadline."""

from datetime import date


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", "Operations Knowledge Base")],
        limit=1,
    )
    if not project:
        return ["Project 'Operations Knowledge Base' not found"]

    original = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Draft launch checklist"),
    ], limit=1)
    if not original:
        failures.append("Original task 'Draft launch checklist' not found")
    else:
        if original.stage_id.name != "To Do":
            failures.append(
                f"Original task stage is '{original.stage_id.name}', expected 'To Do'"
            )
        if original.date_deadline:
            failures.append("Original task should not have a deadline")
        if original.user_ids:
            failures.append("Original task should not have assignees")

    copies = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Draft launch checklist follow-up"),
    ])
    if len(copies) != 1:
        failures.append(
            f"Expected exactly 1 duplicated task, found {len(copies)}"
        )
        return failures

    task = copies[0]
    if task.stage_id.name != "In Progress":
        failures.append(
            f"Duplicated task stage is '{task.stage_id.name}', expected 'In Progress'"
        )
    if task.date_deadline != date(2026, 5, 27):
        failures.append(
            f"Duplicated task deadline is {task.date_deadline}, expected 2026-05-27"
        )
    if "Mitchell Admin" not in task.user_ids.mapped("name"):
        failures.append("Mitchell Admin was not assigned to the duplicated task")

    distractor = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Draft launch checklist mobile"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor task 'Draft launch checklist mobile' not found")
    else:
        if distractor.stage_id.name != "To Do":
            failures.append(
                f"Distractor task stage is '{distractor.stage_id.name}', expected 'To Do'"
            )
        if distractor.date_deadline:
            failures.append("Distractor task should not have a deadline")

    return failures
