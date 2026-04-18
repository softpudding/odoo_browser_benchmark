"""Postcondition checks for project.recurring_task_configure_frequency.

Validates that the seeded task was converted into a weekly recurring
task ending on 2026-06-13.
"""

from datetime import date


PROJECT_NAME = "Bench Recurring Project"
TASK_NAME = "Weekly Status Update"
EXPECTED_INTERVAL = 1
EXPECTED_UNIT = "week"
EXPECTED_TYPE = "until"
EXPECTED_UNTIL = date(2026, 6, 13)


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    task = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
        ("project_id", "=", project.id),
    ], limit=1)
    if not task:
        return [f"Task '{TASK_NAME}' not found in project '{PROJECT_NAME}'"]

    if not task.recurring_task:
        failures.append(
            f"Task '{TASK_NAME}' has recurring_task=False, expected True"
        )

    if task.repeat_interval != EXPECTED_INTERVAL:
        failures.append(
            f"Task '{TASK_NAME}' has repeat_interval={task.repeat_interval}, "
            f"expected {EXPECTED_INTERVAL}"
        )

    if task.repeat_unit != EXPECTED_UNIT:
        failures.append(
            f"Task '{TASK_NAME}' has repeat_unit={task.repeat_unit!r}, "
            f"expected {EXPECTED_UNIT!r}"
        )

    if task.repeat_type != EXPECTED_TYPE:
        failures.append(
            f"Task '{TASK_NAME}' has repeat_type={task.repeat_type!r}, "
            f"expected {EXPECTED_TYPE!r}"
        )

    if task.repeat_until != EXPECTED_UNTIL:
        failures.append(
            f"Task '{TASK_NAME}' has repeat_until={task.repeat_until}, "
            f"expected {EXPECTED_UNTIL.isoformat()}"
        )

    # Project should still exist and not be archived/renamed
    if project.name != PROJECT_NAME:
        failures.append(
            f"Project name changed to '{project.name}', "
            f"expected '{PROJECT_NAME}'"
        )

    return failures
