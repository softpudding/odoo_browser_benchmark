"""Seed for project.close_task_change_state_to_done.

Category: deep_ui_interaction (EASY).

Seeds:
  - project.project 'Bench Close Project' with the three default stages
    ('To Do', 'In Progress', 'Done') pinned via type_ids so the task
    renders in a stable kanban column.
  - project.task 'Review document' on that project with:
      * stage_id = 'To Do' (kanban grouping anchor)
      * state    = '01_in_progress' (In Progress — the default form-header
        state pill label, so the agent has something to click that is NOT
        already Done)
      * priority = '0' (no stars), tag_ids empty, no assignees.

Easy-tier calibration anchor:
  - One widget click + dropdown pick + save.
  - Target: BU-PASS in <60s on ~80% of runs.

Distinct from row 439 (`project.set_task_priority_urgent_assign_tag`):
row 439 targets the **priority** widget (stars) and the `tag_ids` m2m;
this one targets the **state** widget (the rounded-pill dropdown on the
form header introduced/refined in Odoo 19 — `project_task_state_selection`
from `addons/project/.../project_task_state_selection.js`).
"""

PROJECT_NAME = "Bench Close Project"
TASK_NAME = "Review document"


def setup(env):
    # --- Cleanup prior runs -------------------------------------------------
    # 1. Drop the task (by canonical name) so we start from state=in_progress.
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
    ]).unlink()

    # 2. Drop the project (cascade-delete any residual tasks first).
    old_project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in old_project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    old_project.unlink()

    # --- Create fresh project -----------------------------------------------
    project = env["project.project"].create({
        "name": PROJECT_NAME,
    })

    # --- Ensure stages (task needs a stage or it falls into a collapsed
    # 'None' kanban group and disappears from the default kanban view) -------
    stage_names = ["To Do", "In Progress", "Done"]
    stage_map = {}
    for idx, sname in enumerate(stage_names):
        stage = env["project.task.type"].search([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ], limit=1)
        if not stage:
            existing = env["project.task.type"].search(
                [("name", "=", sname)], limit=1
            )
            if existing:
                existing.write({"project_ids": [(4, project.id)]})
                stage = existing
            else:
                stage = env["project.task.type"].create({
                    "name": sname,
                    "sequence": (idx + 1) * 10,
                    "project_ids": [(4, project.id)],
                })
        stage_map[sname] = stage

    # --- Create the seeded task in state 'In Progress' ---------------------
    # NB: `state` has compute='_compute_state' + inverse='_inverse_state' and
    # store=True — writing it directly is supported (the inverse runs), BUT
    # the compute reacts to dependencies (`depend_on_ids` → waiting). Since
    # we have no dependencies, the compute will re-set to '01_in_progress'
    # when recursed — which is exactly what we want. To be belt-and-braces,
    # we write the state explicitly after create.
    task = env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "stage_id": stage_map["To Do"].id,
        "priority": "0",
        "tag_ids": [(5, 0, 0)],
        "description": "Skim the attached document and confirm it is ready to close.",
    })
    # Ensure the visible state pill reads 'In Progress' at seed time.
    task.state = "01_in_progress"

    # --- Sanity assertions --------------------------------------------------
    task_check = env["project.task"].search([("name", "=", TASK_NAME)], limit=1)
    assert task_check, f"seed: task '{TASK_NAME}' not created"
    assert task_check.project_id.name == PROJECT_NAME, (
        f"seed: task not on '{PROJECT_NAME}'"
    )
    assert task_check.state == "01_in_progress", (
        f"seed: task state is '{task_check.state}', expected '01_in_progress'"
    )
    assert task_check.stage_id.name == "To Do", (
        f"seed: stage is '{task_check.stage_id.name}', expected 'To Do'"
    )

    task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    assert task_count == 1, (
        f"seed: expected 1 task on '{PROJECT_NAME}', found {task_count}"
    )
