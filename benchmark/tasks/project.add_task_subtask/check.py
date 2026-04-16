"""Postcondition checks for project.add_task_subtask.

Validates:
1. Main task "Design Landing Page Mockup" exists
2. Subtask "Create Wireframes" exists with correct parent_id
"""

PROJECT_NAME = "Omega Platform Launch"
TASK_NAME = "Design Landing Page Mockup"
SUBTASK_NAME = "Create Wireframes"


def check(env):
    failures = []

    main_task = env["project.task"].search([
        ("name", "=", TASK_NAME),
        ("project_id.name", "=", PROJECT_NAME),
    ], limit=1)

    if not main_task:
        return [f"Task '{TASK_NAME}' in project '{PROJECT_NAME}' not found"]

    subtask = env["project.task"].search([
        ("name", "=", SUBTASK_NAME),
    ], limit=1)

    if not subtask:
        failures.append(f"Subtask '{SUBTASK_NAME}' not found")
    else:
        if not subtask.parent_id:
            failures.append("Subtask has no parent task")
        elif subtask.parent_id.name != TASK_NAME:
            failures.append(f"Subtask parent is '{subtask.parent_id.name}', expected '{TASK_NAME}'")

        if subtask.project_id.name != PROJECT_NAME:
            failures.append(f"Subtask project is '{subtask.project_id.name}', expected '{PROJECT_NAME}'")

    return failures