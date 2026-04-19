"""Postcondition checks for project.close_task_change_state_to_done.

Validates:
1. The 'Review document' project.task still exists (exactly one, active)
   on the 'Bench Close Project' project.
2. state == '1_done' (Done) — was seeded as '01_in_progress' (In Progress).
3. stage_id is unchanged (still 'To Do' — agent must NOT drag or re-pill
   the stage statusbar; only the state widget should be used).
4. priority unchanged at '0' (no stars).
5. Task name is unchanged.
6. Exactly one task on the project (no extras / no deletions).
"""


PROJECT_NAME = "Bench Close Project"
TASK_NAME = "Review document"


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    # 1. Target task exists (exactly one, active).
    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
        ("project_id", "=", project.id),
    ])
    if not tasks:
        failures.append(
            f"Task '{TASK_NAME}' was not found on project '{PROJECT_NAME}'"
        )
        return failures
    if len(tasks) > 1:
        failures.append(
            f"Expected exactly 1 task '{TASK_NAME}', found {len(tasks)}"
        )

    task = tasks[0]
    if not task.active:
        failures.append(f"Task '{TASK_NAME}' is archived (active=False)")

    # 2. state must be '1_done' (was '01_in_progress' in seed). Reject
    # '1_canceled' / '03_approved' / anything else — the prompt is specific.
    if task.state != "1_done":
        failures.append(
            f"Task '{TASK_NAME}' state is '{task.state}', expected '1_done' "
            "(Done) — pick 'Done' from the state widget dropdown, NOT "
            "'Approved' / 'Cancelled' / 'Changes Requested'."
        )

    # 3. stage_id must be unchanged (still 'To Do').
    if task.stage_id.name != "To Do":
        failures.append(
            f"Task '{TASK_NAME}' stage is '{task.stage_id.name}', expected "
            "'To Do' — the prompt forbids changing the kanban stage "
            "(the state widget is independent of stage_id)."
        )

    # 4. priority unchanged at '0' (no stars).
    if task.priority != "0":
        failures.append(
            f"Task '{TASK_NAME}' priority is '{task.priority}', expected '0' "
            "(no priority stars) — priority must not be touched."
        )

    # 5. Task name unchanged.
    if task.name != TASK_NAME:
        failures.append(
            f"Task name is '{task.name}', expected '{TASK_NAME}' (name must "
            "not be changed)."
        )

    # 6. Exactly one task on the project.
    project_task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    if project_task_count != 1:
        failures.append(
            f"Project '{PROJECT_NAME}' has {project_task_count} tasks, expected 1"
        )

    return failures
