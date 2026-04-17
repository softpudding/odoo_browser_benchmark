"""Seed for hr_holidays.request_annual_leave.

Ensure Paid Time Off leave type exists and admin employee has an allocation
so they can submit a 3-day leave request.
"""


LEAVE_NAME = "Family vacation to Iceland"
LEAVE_TYPE = "Paid Time Off"


def setup(env):
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    for leave in prior:
        if leave.state == "validate":
            leave.action_refuse()
            leave.action_draft()
        elif leave.state in ("confirm", "validate1"):
            leave.action_draft()
    prior.unlink()

    admin = env.ref("base.user_admin")
    admin_employee = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if not admin_employee:
        admin_employee = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
        })

    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE)], limit=1
    )
    if not leave_type:
        leave_type = env["hr.leave.type"].create({
            "name": LEAVE_TYPE,
            "requires_allocation": True,
            "leave_validation_type": "manager",
        })
    else:
        leave_type.write({
            "requires_allocation": True,
            "leave_validation_type": "manager",
        })

    existing_alloc = env["hr.leave.allocation"].with_context(
        active_test=False
    ).search([
        ("employee_id", "=", admin_employee.id),
        ("holiday_status_id", "=", leave_type.id),
        ("state", "=", "validate"),
    ])
    if sum(existing_alloc.mapped("number_of_days")) < 10:
        alloc = env["hr.leave.allocation"].create({
            "name": "Annual allocation for admin",
            "holiday_status_id": leave_type.id,
            "employee_id": admin_employee.id,
            "number_of_days": 20,
            "allocation_type": "regular",
            "date_from": "2026-01-01",
        })
        if alloc.state == "draft":
            alloc.action_confirm()
        if alloc.state == "confirm":
            alloc.action_approve()
