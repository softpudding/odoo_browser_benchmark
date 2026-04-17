"""Seed for hr_holidays.refuse_leave_request."""

LEAVE_NAME = "Unscheduled absence — please refuse"


def setup(env):
    admin = env.ref("base.user_admin")

    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    for l in prior:
        if l.state in ("validate", "confirm", "validate1", "refuse"):
            try:
                l.action_draft()
            except Exception:
                pass
    prior.unlink()

    emp_user = env["res.users"].search([("login", "=", "demo")], limit=1)
    if not emp_user:
        emp_user = env["res.users"].create({
            "name": "Marc Demo",
            "login": "demo",
            "password": "demo",
            "group_ids": [(4, env.ref("base.group_user").id)],
        })
    employee = env["hr.employee"].search([("user_id", "=", emp_user.id)], limit=1)
    if not employee:
        employee = env["hr.employee"].create({
            "name": emp_user.name,
            "user_id": emp_user.id,
        })
    employee.write({"leave_manager_id": admin.id})

    ptype = env["hr.leave.type"].search([("name", "=", "Paid Time Off")], limit=1)
    if not ptype:
        ptype = env["hr.leave.type"].create({
            "name": "Paid Time Off",
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })
    else:
        ptype.write({
            "requires_allocation": False,
            "leave_validation_type": "manager",
            "request_unit": "day",
        })

    leave = env["hr.leave"].with_user(emp_user).create({
        "name": LEAVE_NAME,
        "holiday_status_id": ptype.id,
        "employee_id": employee.id,
        "request_date_from": "2026-06-22",
        "request_date_to": "2026-06-22",
    })
    if leave.state == "draft":
        leave.action_confirm()
