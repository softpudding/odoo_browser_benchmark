"""Postcondition checks for project.create_kanban_stage_reorder_drag.

Validates:
1. 'Backlog Review' project.task.type exists.
2. It is linked to 'Bench Project A' (project_ids contains that project).
3. When the project's stages are ordered by (sequence, id) -- the kanban
   grouping order -- 'Backlog Review' sits at position #2 (0-indexed 1).
   i.e. the left-to-right column order is:
      Triage, Backlog Review, In Progress, Review, Done.
4. No pre-existing stage was deleted or renamed.
5. No tasks were created on the project (prompt forbids this).
"""


PROJECT_NAME = "Bench Project A"
NEW_STAGE_NAME = "Backlog Review"
EXISTING_STAGE_NAMES = ["Triage", "In Progress", "Review", "Done"]
EXPECTED_ORDER = [
    "Triage",
    "Backlog Review",
    "In Progress",
    "Review",
    "Done",
]


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    # (1) & (2): new stage exists and is scoped to the project.
    new_stage = env["project.task.type"].with_context(active_test=False).search([
        ("name", "=", NEW_STAGE_NAME),
        ("project_ids", "in", [project.id]),
    ], limit=1)
    if not new_stage:
        failures.append(
            f"New stage '{NEW_STAGE_NAME}' not found on project '{PROJECT_NAME}'"
        )

    # (4): every originally-seeded stage is still there, unchanged.
    for sname in EXISTING_STAGE_NAMES:
        stage = env["project.task.type"].with_context(active_test=False).search([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ], limit=1)
        if not stage:
            failures.append(
                f"Pre-existing stage '{sname}' missing from project "
                f"'{PROJECT_NAME}' (must not be renamed or deleted)"
            )
        elif not stage.active:
            failures.append(
                f"Pre-existing stage '{sname}' is archived (must stay active)"
            )

    # If we already lost the new stage, don't bother checking order.
    if new_stage:
        # (3) ordering. Use the same order the kanban uses: (sequence, id).
        stages = env["project.task.type"].with_context(active_test=False).search([
            ("project_ids", "in", [project.id]),
        ], order="sequence, id")
        actual_order = [s.name for s in stages]

        if actual_order != EXPECTED_ORDER:
            failures.append(
                "Stage left-to-right order is "
                f"{actual_order}; expected {EXPECTED_ORDER}. "
                "'Backlog Review' must sit at position #2 "
                "(between 'Triage' and 'In Progress')."
            )

    # (5): no tasks created on this project.
    task_count = env["project.task"].with_context(active_test=False).search_count([
        ("project_id", "=", project.id),
    ])
    if task_count != 0:
        failures.append(
            f"Expected 0 tasks on '{PROJECT_NAME}' but found {task_count}; "
            "prompt forbids creating any task records."
        )

    return failures
