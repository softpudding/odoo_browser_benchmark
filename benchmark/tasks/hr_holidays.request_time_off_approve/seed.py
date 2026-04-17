"""Seed for hr_holidays.request_time_off_approve.

Category 2 (MEDIUM): Approve a pending time-off request.
The agent must navigate to the manager approval view, find the correct
pending request, and approve it.
"""


def setup(env):
    # Cleanup prior runs
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Medical appointment recovery"),
    ])
    if prior:
        for leave in prior:
            if leave.state == "validate":
                leave.action_refuse()
                leave.action_draft()
            elif leave.state in ("confirm", "validate1"):
                leave.action_draft()
        prior.unlink()

    admin = env.ref("base.user_admin")

    # Ensure admin is a Time Off Administrator so they can approve all leaves
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",      # Time Off Officer
        "hr_holidays.group_hr_holidays_manager",    # Time Off Administrator
        "hr_holidays.group_hr_holidays_responsible", # Time Off Responsible
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Create a separate employee (not the admin) to request leave
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

    # Set the employee's leave manager to admin
    admin_employee = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if admin_employee:
        employee.write({"leave_manager_id": admin.id})

    # Get Sick Time Off leave type — set to manager validation so admin can approve
    sick = env["hr.leave.type"].search([("name", "=", "Sick Time Off")], limit=1)
    if not sick:
        sick = env["hr.leave.type"].create({
            "name": "Sick Time Off",
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })
    else:
        # Override to manager validation so admin (as leave manager) can approve
        sick.write({"leave_validation_type": "manager"})

    # Create the leave request in confirmed state (as the employee)
    leave = env["hr.leave"].with_user(emp_user).create({
        "name": "Medical appointment recovery",
        "holiday_status_id": sick.id,
        "employee_id": employee.id,
        "request_date_from": "2026-06-09",
        "request_date_to": "2026-06-11",
    })
    # The leave auto-enters 'confirm' state on create
    if leave.state == "draft":
        leave.action_confirm()
