"""Seed for hr_holidays.allocate_sick_leave_to_employee.

Category: simple_edit (EASY).
Admin must allocate 15 days of Sick Time Off to employee Marc Demo and
validate the allocation.

Seed ensures:
- Marc Demo employee + user exist
- 'Sick Time Off' leave type exists and requires allocation
- No pre-existing allocation with the description '2026 Sick leave pool'
"""


def setup(env):
    admin = env.ref("base.user_admin")

    # Make sure admin has Time Off administrator rights to approve allocations.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # Cleanup prior runs — any allocation with the target description.
    prior_allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", "2026 Sick leave pool"),
    ])
    for alloc in prior_allocs:
        if alloc.state == "validate":
            alloc.action_refuse()
        if alloc.state in ("confirm", "validate1", "refuse"):
            try:
                alloc.action_draft()
            except Exception:
                pass
    prior_allocs.unlink()

    # Ensure Marc Demo employee + user exists.
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

    # Ensure Sick Time Off leave type exists and requires allocation so that
    # the allocation is meaningful.
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
        })

    # Sanity: ensure the employee's leave_manager_id routes to admin so admin
    # can approve without blocked dependencies.
    employee.write({"leave_manager_id": admin.id})
