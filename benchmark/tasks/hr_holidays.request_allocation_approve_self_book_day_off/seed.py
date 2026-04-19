"""Seed for hr_holidays.request_allocation_approve_self_book_day_off.

HARD (tier 3): Agent must complete a two-phase allocation-then-leave workflow
where the ORDER is critical (allocation must be approved before the leave can
validate).

We seed:
  - A `Bench Bonus Days` leave type with requires_allocation='yes' and
    allocation_validation_type='officer' so the allocation goes through a
    Confirm → Approve lifecycle.
  - A `Bench Worker` employee/user reporting to admin (parent_id =
    admin.employee_id) so admin (as leave_manager / department manager) has
    authority to approve both the allocation and the leave.

We DO NOT pre-create the allocation or leave — the agent must create both.
"""


LEAVE_TYPE_NAME = "Bench Bonus Days"
EMPLOYEE_NAME = "Bench Worker"
EMPLOYEE_LOGIN = "bench_worker"

ALLOC_DESC = "Q2 bonus"
LEAVE_DESC = "Bench day off"


def _drop_prior_records(env):
    """Remove any allocations/leaves left over from prior runs so the seed
    is idempotent.
    """
    prior_leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", [LEAVE_DESC]),
    ])
    for leave in prior_leaves:
        try:
            if leave.state == "validate":
                leave.action_refuse()
        except Exception:
            pass
        try:
            if leave.state in ("confirm", "validate1", "refuse"):
                leave.action_draft()
        except Exception:
            pass
    prior_leaves.unlink()

    prior_allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "in", [ALLOC_DESC]),
    ])
    for alloc in prior_allocs:
        try:
            if alloc.state == "validate":
                alloc.action_refuse()
        except Exception:
            pass
        try:
            if alloc.state in ("confirm", "validate1", "refuse"):
                alloc.action_draft()
        except Exception:
            pass
    prior_allocs.unlink()


def setup(env):
    admin = env.ref("base.user_admin")

    # Grant admin the Time Off Administrator groups so they can approve anyone.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    # Make sure admin has an employee record — parent_id on Bench Worker
    # must point to admin.employee_id.
    admin_emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if not admin_emp:
        admin_emp = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
        })

    # Create / reset the custom leave type.
    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE_NAME)], limit=1
    )
    type_vals = {
        "name": LEAVE_TYPE_NAME,
        "requires_allocation": "yes",
        "allocation_validation_type": "hr",
        "leave_validation_type": "hr",
        "request_unit": "day",
    }
    if leave_type:
        leave_type.write(type_vals)
    else:
        leave_type = env["hr.leave.type"].create(type_vals)

    # Create / refresh the Bench Worker user + employee with admin as parent.
    user = env["res.users"].search([("login", "=", EMPLOYEE_LOGIN)], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": EMPLOYEE_NAME,
            "login": EMPLOYEE_LOGIN,
            "password": EMPLOYEE_LOGIN,
            "group_ids": [(4, env.ref("base.group_user").id)],
        })
    if user.name != EMPLOYEE_NAME:
        user.sudo().write({"name": EMPLOYEE_NAME})

    employee = env["hr.employee"].search([("user_id", "=", user.id)], limit=1)
    emp_vals = {
        "name": EMPLOYEE_NAME,
        "user_id": user.id,
        "parent_id": admin_emp.id,
        "leave_manager_id": admin.id,
    }
    if not employee:
        employee = env["hr.employee"].create(emp_vals)
    else:
        employee.sudo().write(emp_vals)

    # Drop any prior leftover allocation / leave from previous runs so the
    # agent is creating from scratch.
    _drop_prior_records(env)
