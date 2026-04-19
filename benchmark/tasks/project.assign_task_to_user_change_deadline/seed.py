"""Seed for project.assign_task_to_user_change_deadline.

Category: deep_ui_interaction (MEDIUM).

Seeds:
  - project.project 'Bench Assign Project' with the three default stages
    ('To Do', 'In Progress', 'Done') pinned via project_ids so the task
    renders in a stable kanban column.
  - project.task 'Bench Assign Task' on that project with:
      * stage_id = 'To Do' (kanban grouping anchor)
      * user_ids = [] (no assignees — agent must add 'Bench Dev')
      * date_deadline = False (no deadline — agent must set 2026-06-30)
      * priority = '0', tag_ids empty, no description noise.
  - res.users 'Bench Dev' (login 'bench_dev') with base.group_user +
    project.group_project_user so the user is pickable in task.user_ids.

Calibration risks (medium tier):
  * date_deadline picker popover: if the agent doesn't press Tab (or click
    away) the NEXT click may land on the picker instead of the Assignees
    input (or a blurred save).
  * user_ids m2m autocomplete: agent may accidentally quick-create a new
    'Bench Dev' user via the 'Create "Bench Dev" as new user...' row
    instead of picking the existing one.

Distinct from:
  * Row 409 (project.create_task_with_deadline_tags_assignees) — creates a
    brand-new task from scratch with deadline + tags + TWO assignees.
  * Row 439 (project.set_task_priority_urgent_assign_tag) — only priority
    + tag; no date or user m2m.
"""

PROJECT_NAME = "Bench Assign Project"
TASK_NAME = "Bench Assign Task"
DEV_LOGIN = "bench_dev"
DEV_NAME = "Bench Dev"


def setup(env):
    # --- Cleanup prior runs -------------------------------------------------
    # 1. Drop the task (by canonical name) so we start with no deadline/user.
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

    # 3. Drop the seeded dev user (by login) so we can recreate with the
    #    right group membership.
    old_dev = env["res.users"].with_context(active_test=False).search([
        ("login", "=", DEV_LOGIN),
    ])
    if old_dev:
        partners = old_dev.mapped("partner_id")
        old_dev.unlink()
        for partner in partners:
            if partner.name == DEV_NAME:
                try:
                    partner.unlink()
                except Exception:
                    # partner may still be referenced from message_follower etc;
                    # leaving it is harmless.
                    pass

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

    # --- Create the Bench Dev user with project internal-user group --------
    group_project_user = env.ref("project.group_project_user")
    group_internal = env.ref("base.group_user")
    env["res.users"].create({
        "name": DEV_NAME,
        "login": DEV_LOGIN,
        "password": DEV_LOGIN,
        "group_ids": [(6, 0, [group_internal.id, group_project_user.id])],
    })

    # --- Create the seeded task with no assignees and no deadline ----------
    env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "stage_id": stage_map["To Do"].id,
        "priority": "0",
        "tag_ids": [(5, 0, 0)],
        "user_ids": [(5, 0, 0)],
        "date_deadline": False,
    })

    # --- Sanity assertions --------------------------------------------------
    task = env["project.task"].search([("name", "=", TASK_NAME)], limit=1)
    assert task, f"seed: task '{TASK_NAME}' not created"
    assert task.project_id.name == PROJECT_NAME, (
        f"seed: task not on '{PROJECT_NAME}'"
    )
    assert not task.user_ids, (
        f"seed: task should start with NO assignees, "
        f"has {task.user_ids.mapped('login')}"
    )
    assert not task.date_deadline, (
        f"seed: task should start with NO deadline, "
        f"has {task.date_deadline!r}"
    )
    assert task.stage_id.name == "To Do", (
        f"seed: stage is '{task.stage_id.name}', expected 'To Do'"
    )

    dev = env["res.users"].search([("login", "=", DEV_LOGIN)], limit=1)
    assert dev, f"seed: user '{DEV_LOGIN}' not created"
    assert group_project_user in dev.group_ids, (
        f"seed: '{DEV_NAME}' missing project.group_project_user"
    )

    task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    assert task_count == 1, (
        f"seed: expected 1 task on '{PROJECT_NAME}', found {task_count}"
    )
