"""Seed for hr_holidays.cancel_approved_leave_and_reallocate.

Category: recovery_rollback (HARD).
Admin finds an already-approved leave, refuses it, then creates a new
approved replacement leave for different dates.

Seed creates a validated leave for Marc Demo with description
'Family vacation (tentative)' dated 2026-07-06..2026-07-10.
"""


def setup(env):
    admin = env.ref("base.user_admin")

    # Ensure admin is a Time Off administrator.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Cleanup prior runs for both target descriptions.
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", [
            "Family vacation (tentative)",
            "Family vacation (confirmed)",
        ]),
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

    # Ensure Marc Demo employee exists.
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

    # Ensure Paid Time Off leave type doesn't require allocation (so we can
    # create leaves without pre-seeding one) and is manager-validated.
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

    # Create the already-approved "tentative" leave (July 6-10, 2026).
    leave = env["hr.leave"].with_user(admin).create({
        "name": "Family vacation (tentative)",
        "holiday_status_id": ptype.id,
        "employee_id": employee.id,
        "request_date_from": "2026-07-06",
        "request_date_to": "2026-07-10",
    })
    if leave.state == "draft":
        leave.action_confirm()
    if leave.state == "confirm":
        leave.sudo().action_approve()
    # leave.state should now be 'validate'.
