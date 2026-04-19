"""Postcondition checks for project.assign_task_to_user_change_deadline.

Validates:
1. The 'Bench Assign Task' project.task still exists (exactly one, active)
   on the 'Bench Assign Project' project.
2. user_ids contains the existing 'Bench Dev' user (by login='bench_dev').
3. date_deadline is 2026-06-30 (admin-local date).
4. No duplicate 'Bench Dev' user was quick-created — exactly one res.users
   with login 'bench_dev' exists.
5. stage_id is unchanged (still 'To Do') — the agent must NOT drag the
   task to a different kanban column.
6. priority unchanged at '0' (no stars).
7. Task name unchanged.
8. Exactly one task on the project (no extras / no deletions).

Note: project.task.date_deadline is a Datetime field in Odoo 19 (see
addons/project/models/project_task.py). The browser UI sends the typed date
using the admin user's timezone, and Odoo stores the resulting UTC datetime.
We therefore convert the stored UTC datetime back to the admin's local date
before comparing with EXPECTED_DEADLINE.
"""

from datetime import date


PROJECT_NAME = "Bench Assign Project"
TASK_NAME = "Bench Assign Task"
EXPECTED_DEADLINE = date(2026, 6, 30)
DEV_LOGIN = "bench_dev"
DEV_NAME = "Bench Dev"


def _admin_tz(env):
    import pytz
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def check(env):
    import pytz

    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    tz = _admin_tz(env)

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

    # 2. user_ids must contain the existing 'Bench Dev' user (by login).
    user_logins = {u.login for u in task.user_ids}
    if DEV_LOGIN not in user_logins:
        failures.append(
            f"Task '{TASK_NAME}' user_ids missing required user "
            f"'{DEV_NAME}' (login='{DEV_LOGIN}'); has logins "
            f"{sorted(user_logins)}"
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
                f"{actual_date.isoformat()}, expected "
                f"{EXPECTED_DEADLINE.isoformat()}"
            )

    # 4. Exactly one 'Bench Dev' user (no quick-create duplicate).
    dev_users = env["res.users"].with_context(active_test=False).search([
        ("login", "=", DEV_LOGIN),
    ])
    if len(dev_users) == 0:
        failures.append(
            f"User '{DEV_NAME}' (login='{DEV_LOGIN}') no longer exists "
            "(prompt forbids deleting/renaming users)"
        )
    elif len(dev_users) > 1:
        failures.append(
            f"Found {len(dev_users)} users with login '{DEV_LOGIN}'; "
            "prompt forbids creating duplicate users"
        )

    # Also catch 'quick-create by name' where the autocomplete creates a
    # brand-new user with a fresh login like 'bench.dev' or 'Bench Dev'
    # linked to a NEW partner named 'Bench Dev'. Count total distinct users
    # with name 'Bench Dev' — there must be exactly one (the seed user).
    name_matches = env["res.users"].with_context(active_test=False).search([
        ("name", "=", DEV_NAME),
    ])
    if len(name_matches) > 1:
        logins = sorted(name_matches.mapped("login"))
        failures.append(
            f"Found {len(name_matches)} users named '{DEV_NAME}' (logins "
            f"{logins}); prompt forbids creating a new user via the "
            "autocomplete quick-create"
        )

    # 5. stage_id must be unchanged (still 'To Do').
    if task.stage_id.name != "To Do":
        failures.append(
            f"Task '{TASK_NAME}' stage is '{task.stage_id.name}', expected "
            "'To Do' — the prompt forbids changing the kanban stage."
        )

    # 6. priority unchanged at '0' (no stars).
    if task.priority != "0":
        failures.append(
            f"Task '{TASK_NAME}' priority is '{task.priority}', expected "
            "'0' (priority must not be touched)"
        )

    # 7. Task name unchanged.
    if task.name != TASK_NAME:
        failures.append(
            f"Task name is '{task.name}', expected '{TASK_NAME}' "
            "(name must not be changed)"
        )

    # 8. Exactly one task on the project.
    project_task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    if project_task_count != 1:
        failures.append(
            f"Project '{PROJECT_NAME}' has {project_task_count} tasks, "
            "expected 1"
        )

    return failures
