"""Postcondition checks for project.duplicate_task_assign_deadline."""


def check(env):
    failures = []

    project = env["project.project"].search([("name", "=", "Launch Enablement Board")], limit=1)
    if not project:
        return ["Project 'Launch Enablement Board' not found"]

    original = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Prepare webinar outline"),
    ], limit=1)
    if not original:
        failures.append("Original task 'Prepare webinar outline' not found")
    else:
        if original.stage_id.name != "To Do":
            failures.append(
                f"Original task stage is '{original.stage_id.name}', expected 'To Do'"
            )
        if original.date_deadline:
            failures.append("Original task should still have no deadline")

    copies = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Prepare webinar outline - APAC"),
    ])
    if len(copies) != 1:
        failures.append(
            f"Expected exactly 1 duplicated APAC task, found {len(copies)}"
        )
    else:
        copy = copies[0]
        if copy.stage_id.name != "In Progress":
            failures.append(
                f"Copied task stage is '{copy.stage_id.name}', expected 'In Progress'"
            )
        if str(copy.date_deadline) not in ("2026-06-23 16:00:00", "2026-06-24"):
            failures.append(
                f"Copied task deadline is {copy.date_deadline}, expected 2026-06-24"
            )

    distractor = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", "Prepare sales deck"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor task 'Prepare sales deck' not found")
    elif distractor.stage_id.name != "To Do":
        failures.append("Distractor task should remain in 'To Do'")

    return failures
