"""Seed for project.set_task_priority_urgent_assign_tag.

Category: deep_ui_interaction (EASY).

Seeds:
  - project.project 'Bench Prio Project' (single task inside).
  - project.task 'Fix critical bug' on that project with priority='0'
    (Normal — star not filled) and NO tags.
  - project.tags 'Bug' that the agent must pick from the tag_ids
    autocomplete (must pick EXISTING, not quick-create a new one).

Easy-tier calibration anchor:
  - Single toggle (priority star) + single m2m tag pick.
  - Target: BU-PASS in <60s on ~80% of runs.
"""

PROJECT_NAME = "Bench Prio Project"
TASK_NAME = "Fix critical bug"
TAG_NAME = "Bug"


def setup(env):
    # --- Cleanup prior runs -------------------------------------------------
    # 1. Drop the task (by canonical name) so we start from a clean priority.
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

    # 3. Drop the seeded tag (by canonical name) — it's benchmark-owned.
    env["project.tags"].with_context(active_test=False).search([
        ("name", "=", TAG_NAME),
    ]).unlink()

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

    # --- Create the 'Bug' tag on project.tags -------------------------------
    env["project.tags"].create({
        "name": TAG_NAME,
    })

    # --- Create the seeded task with Normal priority and no tags -----------
    env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "stage_id": stage_map["To Do"].id,
        "priority": "0",
        "tag_ids": [(5, 0, 0)],
        "description": "Investigate and fix the critical production bug.",
    })

    # --- Sanity assertions --------------------------------------------------
    task = env["project.task"].search([("name", "=", TASK_NAME)], limit=1)
    assert task, f"seed: task '{TASK_NAME}' not created"
    assert task.project_id.name == PROJECT_NAME, (
        f"seed: task not on '{PROJECT_NAME}'"
    )
    assert task.priority == "0", (
        f"seed: task priority is '{task.priority}', expected '0'"
    )
    assert not task.tag_ids, (
        f"seed: task should start with no tags, has {task.tag_ids.mapped('name')}"
    )

    tag = env["project.tags"].search([("name", "=", TAG_NAME)], limit=1)
    assert tag, f"seed: tag '{TAG_NAME}' not created"

    task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    assert task_count == 1, (
        f"seed: expected 1 task on '{PROJECT_NAME}', found {task_count}"
    )
