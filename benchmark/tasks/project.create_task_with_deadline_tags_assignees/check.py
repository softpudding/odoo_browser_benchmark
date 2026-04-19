"""Postcondition checks for project.create_task_with_deadline_tags_assignees.

Validates:
1. The 'Fix login bug' project.task record exists (exactly one, active).
2. It is scoped to project 'Bench Tag Proj'.
3. date_deadline is 2026-06-30 (admin-local date).
4. tag_ids contains BOTH 'urgent' AND 'backend' (by tag name, case-insensitive).
5. user_ids contains BOTH the Administrator AND 'Bench Dev 2' (by login).
6. No pre-existing tag was deleted/renamed; no duplicate 'urgent'/'backend'
   tags were created (prompt forbids creating new tags).
7. The 'Bench Dev 2' user still exists.
8. No extra tasks were created on the project.

Note: project.task.date_deadline is a Datetime field in Odoo 19. The browser
UI sends the typed date using the admin user's timezone, and Odoo stores the
resulting UTC datetime. We therefore convert the stored UTC datetime back
to the admin's local date before comparing with EXPECTED_DEADLINE.
"""

from datetime import date


PROJECT_NAME = "Bench Tag Proj"
TASK_NAME = "Fix login bug"
EXPECTED_DEADLINE = date(2026, 6, 30)
REQUIRED_TAG_NAMES = {"urgent", "backend"}
DEV2_LOGIN = "bench_dev_2"
ADMIN_LOGIN = "admin"


def _admin_tz(env):
    import pytz
    admin = env["res.users"].search([("login", "=", ADMIN_LOGIN)], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def check(env):
    import pytz

    failures = []

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    tz = _admin_tz(env)

    # 1. New task exists (and exactly one).
    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
    ])
    if not tasks:
        failures.append(f"Task '{TASK_NAME}' was not created")
        return failures
    if len(tasks) > 1:
        failures.append(
            f"Expected exactly 1 task '{TASK_NAME}', found {len(tasks)}"
        )
        # Continue with the first so we can still report other issues.

    task = tasks[0]
    if not task.active:
        failures.append(f"Task '{TASK_NAME}' is archived (active=False)")

    # 2. Scoped to the benchmark project.
    if task.project_id.id != project.id:
        failures.append(
            f"Task '{TASK_NAME}' is on project '{task.project_id.name}', "
            f"expected '{PROJECT_NAME}'"
        )

    # 3. date_deadline (Datetime in Odoo 19 — convert UTC -> admin-local date).
    if not task.date_deadline:
        failures.append(
            f"Task '{TASK_NAME}' has no date_deadline "
            f"(expected {EXPECTED_DEADLINE.isoformat()})"
        )
    else:
        actual_dt = task.date_deadline
        if hasattr(actual_dt, "hour"):
            actual_date = pytz.UTC.localize(actual_dt).astimezone(tz).date()
        else:
            actual_date = actual_dt
        if actual_date != EXPECTED_DEADLINE:
            failures.append(
                f"Task '{TASK_NAME}' date_deadline (admin-local) is "
                f"{actual_date.isoformat()}, expected {EXPECTED_DEADLINE.isoformat()}"
            )

    # 4. Tag set must include both required tags.
    actual_tag_names = {t.name.lower() for t in task.tag_ids}
    missing_tags = REQUIRED_TAG_NAMES - actual_tag_names
    if missing_tags:
        failures.append(
            f"Task '{TASK_NAME}' is missing required tags: "
            f"{sorted(missing_tags)} (has {sorted(actual_tag_names)})"
        )

    # 5. Assignees must include Administrator AND Bench Dev 2.
    user_logins = {u.login for u in task.user_ids}
    if ADMIN_LOGIN not in user_logins:
        failures.append(
            f"Task '{TASK_NAME}' user_ids missing Administrator "
            f"(login='{ADMIN_LOGIN}'); has logins {sorted(user_logins)}"
        )
    if DEV2_LOGIN not in user_logins:
        failures.append(
            f"Task '{TASK_NAME}' user_ids missing 'Bench Dev 2' "
            f"(login='{DEV2_LOGIN}'); has logins {sorted(user_logins)}"
        )

    # 6. No duplicate 'urgent' / 'backend' tags were created — exactly one of each.
    for tag_name in REQUIRED_TAG_NAMES:
        matches = env["project.tags"].with_context(active_test=False).search([
            ("name", "=ilike", tag_name),
        ])
        if len(matches) == 0:
            failures.append(
                f"Tag '{tag_name}' no longer exists "
                f"(prompt forbids deleting/renaming tags)"
            )
        elif len(matches) > 1:
            failures.append(
                f"Found {len(matches)} tags named '{tag_name}'; "
                "prompt forbids creating duplicate tags"
            )

    # 7. Bench Dev 2 still exists.
    dev2 = env["res.users"].with_context(active_test=False).search([
        ("login", "=", DEV2_LOGIN),
    ])
    if not dev2:
        failures.append(
            f"User '{DEV2_LOGIN}' is missing (must not be deleted)"
        )

    # 8. Exactly one task on the project (no stray phantom tasks).
    project_task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    if project_task_count != 1:
        failures.append(
            f"Project '{PROJECT_NAME}' has {project_task_count} tasks, expected 1"
        )

    return failures
