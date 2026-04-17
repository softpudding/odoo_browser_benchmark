"""Seed for hr_holidays.request_half_day_morning.

Category: deep_ui_interaction (EASY).
Admin requests a half-day morning leave for June 15 2026.

Seed ensures:
- Paid Time Off leave type exists and allows half-day and doesn't require
  a pre-allocation (so the request is immediately possible).
- No prior request with the unique description exists.
"""


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs by the unique description.
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Doctor appointment"),
    ])
    for leave in prior:
        if leave.state == "validate":
            try:
                leave.action_refuse()
            except Exception:
                pass
        if leave.state in ("confirm", "validate1", "refuse"):
            try:
                leave.action_draft()
            except Exception:
                pass
    prior.unlink()

    # Ensure admin has an employee record; otherwise create one.
    admin_employee = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if not admin_employee:
        admin_employee = env["hr.employee"].create({
            "name": admin.name,
            "user_id": admin.id,
        })

    # Ensure Paid Time Off leave type exists, supports half-days, and does
    # not require a pre-allocation (so the request can be confirmed easily).
    ptype = env["hr.leave.type"].search([("name", "=", "Paid Time Off")], limit=1)
    if not ptype:
        ptype = env["hr.leave.type"].create({
            "name": "Paid Time Off",
            "requires_allocation": False,
            "request_unit": "half_day",
            "leave_validation_type": "manager",
        })
    else:
        ptype.write({
            "requires_allocation": False,
            "request_unit": "half_day",
        })
