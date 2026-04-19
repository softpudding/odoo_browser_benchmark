"""Seed for project.complete_project_stage_reach_done_percent.

Category: deep_ui_interaction (MEDIUM).

Seeds:
  - project.project 'Bench Progress Project' with three stages pinned
    via project_ids m2m: 'To Do' (seq=10), 'In Progress' (seq=20),
    'Done' (seq=30). Stages must be scoped to the project so the
    kanban view renders all three columns (empty-by-default columns
    are still displayed when pinned via project_ids, per Odoo 19
    project.task.type.group_expand behaviour).
  - Three project.task rows: 'Task A', 'Task B', 'Task C', all with
    stage_id='To Do'. Priority '0', no tags, no assignees, no deadline.

Agent must drag each of the three cards from 'To Do' to 'Done' in the
kanban view (bulk stage change — project.task has no cog Action
'Change Stage', per ODOO19_PATTERNS line 984-996).

Distinct from:
  * Row 448 (project.close_task_change_state_to_done) — clicks the
    task-form state widget to flip state='1_done' on a SINGLE task.
    This row flips stage_id on THREE tasks via the kanban grouping.
  * Row 449 (project.kanban_drag_task_between_stages) — single-card
    drag to 'In Progress' (easy / tier 1). This row is three-card
    drag to 'Done' (medium / tier 2).
"""

PROJECT_NAME = "Bench Progress Project"
TASK_NAMES = ["Task A", "Task B", "Task C"]
STAGE_SEQUENCE = [
    ("To Do", 10),
    ("In Progress", 20),
    ("Done", 30),
]


def setup(env):
    # --- Cleanup prior runs -------------------------------------------------
    # 1. Drop any tasks matching our canonical names anywhere (belt + braces;
    #    a prior run with a different project may have left orphans).
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", TASK_NAMES),
    ]).unlink()

    # 2. Drop the project (cascade-delete any residual tasks first).
    old_project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in old_project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
        # Unlink stages scoped only to this project (m2m).
        stages_scoped = env["project.task.type"].with_context(active_test=False).search([
            ("project_ids", "in", [p.id]),
        ])
        for stage in stages_scoped:
            stage.write({"project_ids": [(3, p.id)]})
    old_project.unlink()

    # --- Create fresh project -----------------------------------------------
    project = env["project.project"].create({
        "name": PROJECT_NAME,
    })

    # --- Ensure stages, scoped to this project, with deterministic sequences
    # so the kanban columns render left-to-right as: To Do | In Progress | Done
    stage_map = {}
    for sname, seq in STAGE_SEQUENCE:
        stage = env["project.task.type"].search([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ], limit=1)
        if not stage:
            # Prefer linking an existing global stage over creating a new
            # one with a colliding name, to keep the stage pool clean.
            existing = env["project.task.type"].search(
                [("name", "=", sname)], limit=1
            )
            if existing:
                existing.write({
                    "project_ids": [(4, project.id)],
                    "sequence": seq,
                })
                stage = existing
            else:
                stage = env["project.task.type"].create({
                    "name": sname,
                    "sequence": seq,
                    "project_ids": [(6, 0, [project.id])],
                })
        stage_map[sname] = stage

    # --- Create the three tasks, all in 'To Do' -----------------------------
    todo = stage_map["To Do"]
    for tname in TASK_NAMES:
        env["project.task"].create({
            "name": tname,
            "project_id": project.id,
            "stage_id": todo.id,
            "priority": "0",
            "tag_ids": [(5, 0, 0)],
            "user_ids": [(5, 0, 0)],
        })

    # --- Sanity assertions --------------------------------------------------
    tasks = env["project.task"].search([
        ("project_id", "=", project.id),
    ])
    assert len(tasks) == 3, (
        f"seed: expected 3 tasks on '{PROJECT_NAME}', found {len(tasks)}"
    )
    names = sorted(tasks.mapped("name"))
    assert names == sorted(TASK_NAMES), (
        f"seed: task names {names}, expected {sorted(TASK_NAMES)}"
    )
    for t in tasks:
        assert t.stage_id.name == "To Do", (
            f"seed: task '{t.name}' stage is '{t.stage_id.name}', "
            f"expected 'To Do'"
        )

    # Verify all three stages are linked to the project.
    for sname, _ in STAGE_SEQUENCE:
        linked = env["project.task.type"].search_count([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ])
        assert linked >= 1, (
            f"seed: stage '{sname}' not linked to '{PROJECT_NAME}'"
        )
