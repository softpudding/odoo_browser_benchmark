"""Seed a project with one non-recurring task that the agent must convert.

Category: deep_ui_interaction (MEDIUM).

Capability tested: Toggling a boolean (Recurrent) and configuring the
revealed sub-form (Repeat Every / Weeks / Until / End Date) on a
project.task. The recurring-tasks feature gate
(`project.group_project_recurring_tasks`) must be granted to admin and
the project must have `allow_recurring_tasks=True` so the UI exposes
the controls.
"""

PROJECT_NAME = "Bench Recurring Project"
TASK_NAME = "Weekly Status Update"


def setup(env):
    # --- Cleanup prior runs ---
    stale_tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
    ])
    if stale_tasks:
        # Drop any recurrence rows so we delete cleanly
        recurrences = stale_tasks.mapped("recurrence_id")
        stale_tasks.write({"recurring_task": False, "recurrence_id": False})
        if recurrences:
            recurrences.unlink()
        stale_tasks.unlink()

    stale_projects = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    if stale_projects:
        leftover_tasks = env["project.task"].with_context(active_test=False).search([
            ("project_id", "in", stale_projects.ids),
        ])
        if leftover_tasks:
            recurrences = leftover_tasks.mapped("recurrence_id")
            leftover_tasks.write({"recurring_task": False, "recurrence_id": False})
            if recurrences:
                recurrences.unlink()
            leftover_tasks.unlink()
        stale_projects.unlink()

    # --- Ensure admin has the "Use Recurring Tasks" group ---
    group = env.ref("project.group_project_recurring_tasks", raise_if_not_found=False)
    if group:
        admin = env.ref("base.user_admin", raise_if_not_found=False)
        if admin and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # --- Create fresh project with recurring tasks enabled ---
    project = env["project.project"].create({
        "name": PROJECT_NAME,
        "allow_recurring_tasks": True,
    })

    # --- Create the single non-recurring task ---
    env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "recurring_task": False,
    })
