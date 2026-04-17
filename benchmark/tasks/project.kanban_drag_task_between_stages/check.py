"""Postcondition checks for project.kanban_drag_task_between_stages.

Validates:
1. 'Benchmark Card Alpha' now sits in the 'In Progress' stage.
2. 'Benchmark Card Beta' was NOT moved — still in 'To Do'.
3. Both tasks still belong to the 'Benchmark Drag Project'.
4. Neither task was renamed.
"""


PROJECT_NAME = "Benchmark Drag Project"
ALPHA_NAME = "Benchmark Card Alpha"
BETA_NAME = "Benchmark Card Beta"


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    alpha = env["project.task"].with_context(active_test=False).search([
        ("name", "=", ALPHA_NAME),
        ("project_id", "=", project.id),
    ], limit=1)
    if not alpha:
        failures.append(f"Task '{ALPHA_NAME}' not found in project")
    else:
        stage_name = alpha.stage_id.name if alpha.stage_id else None
        if stage_name != "In Progress":
            failures.append(
                f"Task '{ALPHA_NAME}' stage is '{stage_name}', "
                "expected 'In Progress'"
            )

    beta = env["project.task"].with_context(active_test=False).search([
        ("name", "=", BETA_NAME),
        ("project_id", "=", project.id),
    ], limit=1)
    if not beta:
        failures.append(f"Sibling task '{BETA_NAME}' is missing")
    else:
        stage_name = beta.stage_id.name if beta.stage_id else None
        if stage_name != "To Do":
            failures.append(
                f"Sibling task '{BETA_NAME}' stage is '{stage_name}', "
                "expected still in 'To Do'"
            )

    return failures
