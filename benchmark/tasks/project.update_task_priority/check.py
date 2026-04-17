"""Postcondition checks for project.update_task_priority."""


def check(env):
    failures = []

    project = env["project.project"].search([("name", "=", "Astra Feature Rollout")], limit=1)
    if not project:
        return ["Project 'Astra Feature Rollout' not found"]

    task = env["project.task"].search([
        ("name", "=", "Validate release notes"),
        ("project_id", "=", project.id),
    ], limit=1)
    if not task:
        return ["Task 'Validate release notes' not found in project"]

    if task.priority != "1":
        failures.append(
            f"Priority is '{task.priority}', expected '1' (Important)"
        )

    return failures
