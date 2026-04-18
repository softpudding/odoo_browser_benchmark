"""Seed for project.create_kanban_stage_reorder_drag.

Category: deep_ui_interaction (MEDIUM).

Seeds a project ('Bench Project A') with four pre-existing task stages
scoped to that project: Triage, In Progress, Review, Done (sequences
10, 20, 30, 40 respectively). The benchmark task then asks the agent
to CREATE a fifth stage 'Backlog Review' via the kanban column
quick-create ('+' / 'Add column'), and DRAG-REORDER it to position
#2 (between Triage and In Progress).

Calibration risk (flagged): the kanban column drag-reorder uses Owl's
useSortable / web_resequence. Browser-use's drag gesture sometimes
fails to trigger the sortable handlers reliably. Human/oracle solves
via a slow emulated mouse drag on the column title handle.
"""

PROJECT_NAME = "Bench Project A"
STAGE_SEQUENCE = [
    ("Triage", 10),
    ("In Progress", 20),
    ("Review", 30),
    ("Done", 40),
]
NEW_STAGE_NAME = "Backlog Review"


def setup(env):
    # --- Cleanup prior runs (child-first, active_test=False for archived rows) ---
    # 1. Drop any stray 'Backlog Review' stages linked only to this project.
    old_new_stage = (
        env["project.task.type"]
        .with_context(active_test=False)
        .search([("name", "=", NEW_STAGE_NAME)])
    )
    if old_new_stage:
        old_new_stage.unlink()

    old_project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if old_project:
        # Delete tasks still linked to the project (safety)
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", old_project.id),
        ]).unlink()
        # Delete stages scoped only to this project (m2m project_ids)
        stages_scoped = env["project.task.type"].with_context(active_test=False).search([
            ("project_ids", "in", [old_project.id]),
        ])
        # Remove the project from each stage; if the stage ends up orphaned
        # (no project_ids) AND it's one of our canonical names, drop it too.
        for stage in stages_scoped:
            stage.write({"project_ids": [(3, old_project.id)]})
            if not stage.project_ids and stage.name in (
                [n for n, _ in STAGE_SEQUENCE] + [NEW_STAGE_NAME]
            ):
                stage.unlink()
        old_project.unlink()

    # --- Create fresh project ---
    project = env["project.project"].create({
        "name": PROJECT_NAME,
    })

    # --- Create the four stages, scoped to this project only, with explicit
    # sequences so the kanban grouping order is deterministic ---
    for sname, seq in STAGE_SEQUENCE:
        env["project.task.type"].create({
            "name": sname,
            "sequence": seq,
            "project_ids": [(6, 0, [project.id])],
        })

    # Sanity check: no 'Backlog Review' stage should be linked to this project.
    assert not env["project.task.type"].with_context(active_test=False).search([
        ("name", "=", NEW_STAGE_NAME),
        ("project_ids", "in", [project.id]),
    ]), f"Unexpected pre-existing '{NEW_STAGE_NAME}' stage on {PROJECT_NAME}"
