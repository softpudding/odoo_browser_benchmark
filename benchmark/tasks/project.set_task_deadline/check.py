"""Postcondition checks for project.set_task_deadline.

Validates that:
1. The task "Design Landing Page Mockup" has deadline set to 2026-05-20
2. The task still exists in the same project
"""


def check(env):
    failures = []

    # Find the target task
    task = env["project.task"].search([
        ("name", "=", "Design Landing Page Mockup"),
    ], limit=1)

    if not task:
        return ["Task 'Design Landing Page Mockup' not found"]

    # Check deadline is set correctly
    expected_deadline = "2026-05-20"
    actual_deadline = str(task.date_deadline) if task.date_deadline else None
    if actual_deadline != expected_deadline:
        failures.append(
            f"Deadline is '{actual_deadline}', expected '{expected_deadline}'"
        )

    # Check project is still correct
    if task.project_id.name != "Omega Platform Launch":
        failures.append(
            f"Project is '{task.project_id.name}', expected 'Omega Platform Launch'"
        )

    return failures