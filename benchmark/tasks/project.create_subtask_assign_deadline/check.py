"""Postcondition checks for project.create_subtask_assign_deadline."""


PROJECT_NAME = "Atlas Implementation Sprint"
PARENT_TASK = "Prepare onboarding checklist"
SUBTASK_NAME = "Draft kickoff agenda"
DISTRACTOR_TASK = "Review onboarding checklist"


def check(env):
    failures = []

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    parent = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", PARENT_TASK),
    ], limit=1)
    distractor = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", DISTRACTOR_TASK),
    ], limit=1)
    if not parent or not distractor:
        return ["Missing seeded tasks for project subtask task"]

    subtasks = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", SUBTASK_NAME),
    ])
    if len(subtasks) != 1:
        return [f"Expected exactly 1 subtask named '{SUBTASK_NAME}', found {len(subtasks)}"]

    subtask = subtasks[0]
    if subtask.parent_id.id != parent.id:
        failures.append(
            f"Subtask parent is {subtask.parent_id.name!r}, expected {PARENT_TASK!r}"
        )
    if "Administrator" not in subtask.user_ids.mapped("name"):
        failures.append("Subtask is not assigned to Administrator")
    if subtask.stage_id.name != "In Progress":
        failures.append(
            f"Subtask stage is {subtask.stage_id.name!r}, expected 'In Progress'"
        )
    deadline_text = str(subtask.date_deadline or "")
    if deadline_text not in ("2026-05-26 16:00:00", "2026-05-27"):
        failures.append(
            f"Subtask deadline is {deadline_text!r}, expected 05/27/2026"
        )
    if parent.date_deadline:
        failures.append("Parent task deadline should remain unset")
    if parent.stage_id.name != "To Do":
        failures.append(f"Parent task stage is {parent.stage_id.name!r}, expected 'To Do'")
    if distractor.stage_id.name != "To Do":
        failures.append(
            f"Distractor task stage is {distractor.stage_id.name!r}, expected 'To Do'"
        )
    if distractor.user_ids:
        failures.append("Distractor task should not have assignees")

    return failures
