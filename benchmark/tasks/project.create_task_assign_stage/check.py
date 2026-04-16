"""Postcondition checks for project.create_task_assign_stage.

Validates:
1. Task "Design Landing Page Mockup" exists in "Omega Platform Launch"
2. Assignee includes Mitchell Admin
3. Deadline is 2026-05-15
4. Priority is "1" (urgent/starred)
5. Description contains expected text
6. Stage is "In Progress"
"""

from datetime import date


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", "Omega Platform Launch")], limit=1
    )
    if not project:
        return ["Project 'Omega Platform Launch' not found"]

    task = env["project.task"].search([
        ("name", "=", "Design Landing Page Mockup"),
        ("project_id", "=", project.id),
    ], limit=1)

    if not task:
        return ["Task 'Design Landing Page Mockup' not found in project"]

    # Check stage
    if not task.stage_id or task.stage_id.name != "In Progress":
        failures.append(
            f"Stage is '{task.stage_id.name if task.stage_id else 'None'}', "
            "expected 'In Progress'"
        )

    # Check assignee
    admin = env.ref("base.user_admin")
    if admin not in task.user_ids:
        assigned = ", ".join(task.user_ids.mapped("name")) or "nobody"
        failures.append(
            f"Assignees: {assigned}; expected Mitchell Admin"
        )

    # Check deadline
    expected_deadline = date(2026, 5, 15)
    if task.date_deadline != expected_deadline:
        failures.append(
            f"Deadline is {task.date_deadline}, expected {expected_deadline}"
        )

    # Check priority
    if task.priority != "1":
        failures.append(
            f"Priority is '{task.priority}', expected '1' (urgent)"
        )

    # Check description
    desc = task.description or ""
    # Strip HTML if present
    import re
    desc_text = re.sub(r"<[^>]+>", "", desc).strip()
    if "wireframes" not in desc_text.lower() or "landing page" not in desc_text.lower():
        failures.append(
            f"Description does not contain expected text about wireframes and landing page"
        )

    return failures
