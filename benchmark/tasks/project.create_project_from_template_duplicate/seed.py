"""Seed a 'Bench Template Project' with three tasks.

Category: deep_ui_interaction (MEDIUM).

Capability tested: Project duplication via the Project kanban card's
Duplicate action (or Actions > Duplicate in the form). Odoo's
``project.project.copy()`` automatically copies the linked
``project.task`` records via ``map_tasks``.
"""

PROJECT_NAME = "Bench Template Project"
COPY_NAME = "Bench Template Project (Copy)"
TASK_NAMES = ["Setup", "Build", "Review"]


def setup(env):
    # --- Cleanup prior runs (both original and any stale copy) ---
    stale_projects = env["project.project"].with_context(active_test=False).search([
        ("name", "in", [PROJECT_NAME, COPY_NAME]),
    ])
    if stale_projects:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "in", stale_projects.ids),
        ]).unlink()
        stale_projects.unlink()

    # Sweep up any tasks that share our seed names but somehow lost their
    # project link from a previous aborted run.
    orphan_tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "in", TASK_NAMES),
        ("project_id", "=", False),
    ])
    if orphan_tasks:
        orphan_tasks.unlink()

    # --- Create fresh template project ---
    project = env["project.project"].create({
        "name": PROJECT_NAME,
    })

    # --- Create three ordered tasks on the template project ---
    for idx, tname in enumerate(TASK_NAMES, start=1):
        env["project.task"].create({
            "name": tname,
            "project_id": project.id,
            "sequence": idx * 10,
        })
