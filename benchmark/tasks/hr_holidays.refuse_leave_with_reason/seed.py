"""Seed a pending Paid Time Off request from Marc Demo for manager refusal."""


LEAVE_NAME = "Personal emergency"


def setup(env):
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    for leave in prior:
        if leave.state == "validate":
            leave.action_refuse()
            leave.action_draft()
        elif leave.state in ("confirm", "validate1", "refuse"):
            leave.action_draft()
    prior.unlink()

    admin = env.ref("base.user_admin")
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

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

    paid = env["hr.leave.type"].search([("name", "=", "Paid Time Off")], limit=1)
    if not paid:
        paid = env["hr.leave.type"].create({
            "name": "Paid Time Off",
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })
    else:
        paid.write({
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })

    leave = env["hr.leave"].with_user(emp_user).create({
        "name": LEAVE_NAME,
        "holiday_status_id": paid.id,
        "employee_id": employee.id,
        "request_date_from": "2026-06-15",
        "request_date_to": "2026-06-17",
    })
    if leave.state == "draft":
        leave.action_confirm()
