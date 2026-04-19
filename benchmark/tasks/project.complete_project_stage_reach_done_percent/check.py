"""Postcondition checks for project.complete_project_stage_reach_done_percent.

Validates:
1. Project 'Bench Progress Project' still exists.
2. Exactly three tasks on the project, with canonical names (Task A,
   Task B, Task C), and they were not renamed.
3. All three tasks have stage_id.name == 'Done'.
4. Three stages ('To Do', 'In Progress', 'Done') are still pinned to
   the project.
5. No extra tasks created; no tasks deleted; no tasks archived.
6. Tasks' project_id still points at the correct project (no one
   moved them to a different project).
"""


PROJECT_NAME = "Bench Progress Project"
TASK_NAMES = ["Task A", "Task B", "Task C"]
STAGE_NAMES = ["To Do", "In Progress", "Done"]


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    # (1) & (2): three tasks exist on the project with canonical names.
    tasks = env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", project.id),
    ])
    if len(tasks) != 3:
        failures.append(
            f"Expected 3 tasks on '{PROJECT_NAME}', found {len(tasks)} "
            f"(names: {sorted(tasks.mapped('name'))})"
        )

    found_names = sorted(tasks.mapped("name"))
    missing = [n for n in TASK_NAMES if n not in found_names]
    if missing:
        failures.append(
            f"Missing tasks on '{PROJECT_NAME}': {missing} "
            f"(present: {found_names})"
        )

    # (3): each seeded task must have stage_id.name == 'Done'.
    for tname in TASK_NAMES:
        t = env["project.task"].with_context(active_test=False).search([
            ("name", "=", tname),
            ("project_id", "=", project.id),
        ], limit=1)
        if not t:
            # Already reported above; skip stage check.
            continue
        if not t.active:
            failures.append(
                f"Task '{tname}' is archived (active=False) — tasks "
                "must remain active."
            )
        stage_name = t.stage_id.name if t.stage_id else None
        if stage_name != "Done":
            failures.append(
                f"Task '{tname}' has stage_id '{stage_name}', expected "
                "'Done' — drag the card from 'To Do' to 'Done' in the "
                "kanban view (do NOT use the task-form state widget, "
                "which writes to `state`, not `stage_id`)."
            )

    # (4): the three stages must still be pinned to the project.
    for sname in STAGE_NAMES:
        linked = env["project.task.type"].with_context(active_test=False).search([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ])
        if not linked:
            failures.append(
                f"Stage '{sname}' is no longer linked to '{PROJECT_NAME}' "
                "(prompt forbids deleting or unlinking stages)."
            )

    return failures
