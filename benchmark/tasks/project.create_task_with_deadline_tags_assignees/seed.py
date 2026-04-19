"""Seed for project.create_task_with_deadline_tags_assignees.

Category: deep_ui_interaction (MEDIUM).

Seeds:
  - project.project 'Bench Tag Proj' (empty — zero tasks).
  - project.tags 'urgent' and 'backend' that the agent must pick from the
    tag_ids autocomplete (must pick EXISTING, not quick-create new ones).
  - res.users 'Bench Dev 2' with project.group_project_user so the user is
    pickable in the user_ids m2m on project.task.

Calibration risks:
  * date_deadline: typed date may leave the date-picker popover open; if the
    agent doesn't press Tab (or click away) the NEXT click lands on the
    picker instead of the Tags input.
  * tag_ids m2m autocomplete: agent may pick only the first tag or accidentally
    quick-create a new 'urgent' / 'backend' tag instead of the existing one.
  * user_ids m2m: agent may leave it with the default (creator = Administrator)
    and forget to add the second assignee 'Bench Dev 2'.
"""

PROJECT_NAME = "Bench Tag Proj"
TAG_NAMES = ["urgent", "backend"]
DEV2_LOGIN = "bench_dev_2"
DEV2_NAME = "Bench Dev 2"
NEW_TASK_NAME = "Fix login bug"


def setup(env):
    # --- Cleanup prior runs -------------------------------------------------
    # 1. Drop the new task name so we can reuse the seed reliably.
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", NEW_TASK_NAME),
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

    # 3. Drop the seeded tags (by canonical name) — they're benchmark-owned.
    old_tags = env["project.tags"].with_context(active_test=False).search([
        ("name", "in", TAG_NAMES),
    ])
    old_tags.unlink()

    # 4. Drop the seeded dev user (by login) so we can recreate with the
    #    right group membership.
    old_dev = env["res.users"].with_context(active_test=False).search([
        ("login", "=", DEV2_LOGIN),
    ])
    if old_dev:
        # Also drop the linked partner if safe (name must match, no other refs).
        partners = old_dev.mapped("partner_id")
        old_dev.unlink()
        for partner in partners:
            if partner.name == DEV2_NAME:
                try:
                    partner.unlink()
                except Exception:
                    # partner may still be referenced from message_follower etc;
                    # leaving it is harmless.
                    pass

    # --- Create fresh project -----------------------------------------------
    env["project.project"].create({
        "name": PROJECT_NAME,
    })

    # --- Create the two tags on project.tags --------------------------------
    for tag_name in TAG_NAMES:
        env["project.tags"].create({
            "name": tag_name,
        })

    # --- Create the second dev user with project internal-user group -------
    group_project_user = env.ref("project.group_project_user")
    group_internal = env.ref("base.group_user")
    env["res.users"].create({
        "name": DEV2_NAME,
        "login": DEV2_LOGIN,
        "password": DEV2_LOGIN,
        "group_ids": [(6, 0, [group_internal.id, group_project_user.id])],
    })

    # --- Sanity assertions --------------------------------------------------
    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    assert project, f"seed: project '{PROJECT_NAME}' not created"
    assert env["project.task"].search_count([
        ("project_id", "=", project.id),
    ]) == 0, f"seed: expected 0 tasks in '{PROJECT_NAME}'"

    for tag_name in TAG_NAMES:
        tag = env["project.tags"].search([("name", "=", tag_name)], limit=1)
        assert tag, f"seed: tag '{tag_name}' not created"

    dev2 = env["res.users"].search([("login", "=", DEV2_LOGIN)], limit=1)
    assert dev2, f"seed: user '{DEV2_LOGIN}' not created"
    assert group_project_user in dev2.group_ids, (
        f"seed: '{DEV2_NAME}' missing project.group_project_user"
    )
