"""Postcondition checks for project.update_task_assign_deadline_activity."""

from datetime import date


PROJECT_NAME = "Customer Portal Refresh"
TARGET_TASK = "Revise FAQ copy"
DISTRACTOR_TASK = "Revise API docs"
ACTIVITY_SUMMARY = "Review FAQ revisions"


def check(env):
    failures = []

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    task = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", TARGET_TASK),
    ], limit=1)
    if not task:
        return [f"Task '{TARGET_TASK}' not found"]

    if not task.stage_id or task.stage_id.name != "In Progress":
        failures.append(
            f"Task stage is '{task.stage_id.name if task.stage_id else None}', expected 'In Progress'"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "project.task"),
        ("res_id", "=", task.id),
    ])
    call_activities = activities.filtered(
        lambda act: (
            (act.activity_type_id.name or "") == "Call"
            or act.activity_type_id.category == "phonecall"
            or "call" in (act.activity_type_id.name or "").lower()
        )
        and act.summary == ACTIVITY_SUMMARY
    )
    if not call_activities:
        failures.append("Expected Call activity was not scheduled on the task")
    else:
        activity = call_activities[0]
        if activity.date_deadline != date(2026, 5, 20):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-05-20"
            )

    distractor = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "=", DISTRACTOR_TASK),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor task '{DISTRACTOR_TASK}' not found")
    else:
        if distractor.stage_id and distractor.stage_id.name != "To Do":
            failures.append(
                f"Distractor task moved to '{distractor.stage_id.name}', expected 'To Do'"
            )
        if env["mail.activity"].search_count([
            ("res_model", "=", "project.task"),
            ("res_id", "=", distractor.id),
            ("summary", "=", ACTIVITY_SUMMARY),
        ]):
            failures.append("Distractor task received the target activity")

    return failures
