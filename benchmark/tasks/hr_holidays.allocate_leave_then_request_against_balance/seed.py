"""Seed for hr_holidays.allocate_leave_then_request_against_balance."""


def setup(env):
    admin = env.ref("base.user_admin")

    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    alloc_name = "Quarter-End Sick Leave Buffer"
    leave_name = "Warehouse flu recovery"

    prior_leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", leave_name),
    ])
    for leave in prior_leaves:
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
    prior_leaves.unlink()

    prior_allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", alloc_name),
    ])
    for alloc in prior_allocs:
        if alloc.state == "validate":
            try:
                alloc.action_refuse()
            except Exception:
                pass
        if alloc.state in ("confirm", "validate1", "refuse"):
            try:
                alloc.action_draft()
            except Exception:
                pass
    prior_allocs.unlink()

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

    sick = env["hr.leave.type"].search([("name", "=", "Sick Time Off")], limit=1)
    if not sick:
        sick = env["hr.leave.type"].create({
            "name": "Sick Time Off",
            "requires_allocation": True,
            "allocation_validation_type": "hr",
            "leave_validation_type": "hr",
        })
    else:
        sick.write({
            "requires_allocation": True,
            "allocation_validation_type": "hr",
            "leave_validation_type": "hr",
        })
