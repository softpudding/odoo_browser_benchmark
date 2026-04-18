"""Postcondition checks for project_todo.reorder_notes_add_due_dates_bulk.

Validates:
1. Each of the three seeded notes has the correct date_deadline.
2. None of the three notes was archived, renamed, or deleted.

Note: project.task.date_deadline is a Datetime field in Odoo 19. The
browser UI writes deadlines using the admin user's timezone, which is
stored as a UTC datetime. We therefore convert the stored UTC value
back to the admin's local date before comparing.
"""

from datetime import date


ALPHA = "Benchmark Note Alpha"
BETA = "Benchmark Note Beta"
GAMMA = "Benchmark Note Gamma"

EXPECTED_DEADLINES = {
    ALPHA: date(2026, 4, 25),
    BETA: date(2026, 4, 30),
    GAMMA: date(2026, 5, 2),
}


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

    for name, expected in EXPECTED_DEADLINES.items():
        tasks = env["project.task"].with_context(active_test=False).search([
            ("name", "=", name),
        ])
        if not tasks:
            failures.append(f"Note '{name}' not found")
            continue
        if len(tasks) > 1:
            failures.append(
                f"Expected exactly one note named '{name}', found {len(tasks)}"
            )
            continue
        task = tasks
        if not task.active:
            failures.append(f"Note '{name}' should remain active but was archived")

        if not task.date_deadline:
            failures.append(f"Note '{name}' has no deadline, expected {expected}")
            continue

        actual_dt = task.date_deadline
        # Datetime -> admin-local date
        if hasattr(actual_dt, "hour"):
            actual = pytz.UTC.localize(actual_dt).astimezone(tz).date()
        else:
            actual = actual_dt
        if actual != expected:
            failures.append(
                f"Note '{name}' deadline is {actual}, expected {expected}"
            )

    return failures
