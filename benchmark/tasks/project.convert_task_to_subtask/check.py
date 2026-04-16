"""Postcondition checks for project.convert_task_to_subtask."""


PROJECT_NAME = "Atlas Support Rollout"
TASK_NAME = "Vendor readiness checklist"
PARENT_TASK = "Launch coordination"
DISTRACTOR_TASK = "Archived coordination notes"


def check(env):
    failures = []

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    task = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", TASK_NAME),
    ], limit=1)
    if not task:
        return [f"Task '{TASK_NAME}' not found"]

    if task.parent_id.name != PARENT_TASK:
        failures.append(
            f"Task parent is '{task.parent_id.name}', expected '{PARENT_TASK}'"
        )
    parent = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", PARENT_TASK),
    ], limit=1)
    if not parent:
        failures.append("Parent task not found")
    else:
        if parent.parent_id:
            failures.append(
                "Parent task was converted unexpectedly"
            )

    distractor = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", DISTRACTOR_TASK),
    ], limit=1)
    if distractor and distractor.parent_id:
        failures.append("Distractor task was converted unexpectedly")

    return failures
