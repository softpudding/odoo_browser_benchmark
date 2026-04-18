"""Seed for hr_holidays.approve_leave_as_manager.

Category: deep_ui_interaction (MEDIUM).

Creates a pending Paid Time Off request ("Family event leave") for Marc Demo
that awaits manager validation. Admin is granted Time Off administrator
groups and set as Marc's leave manager, so admin can approve the request
from the Approvals queue.
"""

LEAVE_NAME = "Family event leave"


def setup(env):
    admin = env.ref("base.user_admin")

    # Ensure admin has Time Off administrator/officer/responsible groups so
    # the Approvals menu is visible and the Approve action is allowed.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    # Cleanup prior runs by the unique leave name.
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
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

    # Ensure a distinct employee user (Marc Demo) exists.
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

    # Admin is Marc's leave manager so admin can approve his request.
    employee.write({"leave_manager_id": admin.id})

    # Ensure Paid Time Off exists, allows day requests without allocation,
    # and uses single-level manager validation.
    ptype = env["hr.leave.type"].search([("name", "=", "Paid Time Off")], limit=1)
    if not ptype:
        ptype = env["hr.leave.type"].create({
            "name": "Paid Time Off",
            "requires_allocation": False,
            "request_unit": "day",
            "leave_validation_type": "manager",
        })
    else:
        ptype.write({
            "requires_allocation": False,
            "request_unit": "day",
            "leave_validation_type": "manager",
        })

    # Create the leave request as the employee in 'confirm' state.
    leave = env["hr.leave"].with_user(emp_user).create({
        "name": LEAVE_NAME,
        "holiday_status_id": ptype.id,
        "employee_id": employee.id,
        "request_date_from": "2026-06-17",
        "request_date_to": "2026-06-18",
    })
    if leave.state == "draft":
        leave.action_confirm()
