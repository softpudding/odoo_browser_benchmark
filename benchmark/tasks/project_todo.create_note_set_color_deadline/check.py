"""Postcondition checks for project_todo.create_note_set_color_deadline."""

from datetime import date


TARGET_NAME = "Crane Audit Memo"
EXPECTED_DATE = date(2026, 5, 20)


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
    tz = _admin_tz(env)
    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ])
    if not tasks:
        return [f"Note {TARGET_NAME!r} not found"]
    if len(tasks) != 1:
        return [f"Expected exactly one note named {TARGET_NAME!r}, found {len(tasks)}"]

    task = tasks[0]
    if not task.active:
        failures.append("Note should remain active")
    if task.tag_ids:
        failures.append(f"Note should not have tags but has {task.tag_ids.mapped('name')}")
    if not task.date_deadline:
        failures.append("Note is missing a deadline")
    else:
        actual_dt = task.date_deadline
        actual = pytz.UTC.localize(actual_dt).astimezone(tz).date() if hasattr(actual_dt, "hour") else actual_dt
        if actual != EXPECTED_DATE:
            failures.append(f"Deadline date is {actual}, expected {EXPECTED_DATE}")
    if (task.color or 0) == 0:
        failures.append("Note still has the default color; expected a non-default kanban color")

    return failures
