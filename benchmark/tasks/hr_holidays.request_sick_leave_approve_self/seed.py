"""Seed for hr_holidays.request_sick_leave_approve_self.

HARD (tier 3): Agent must perform a two-step role lifecycle (submit + approve)
for a sick leave request. The seed provides:

  - A `Sick Leave` leave type with `requires_allocation='no'` (no allocation
    needed to book sick days) and `leave_validation_type='hr'` so an HR / Time
    Off manager must explicitly Approve the pending request for it to reach
    `validate`.
  - A `Bench Sick Employee` user + employee reporting to admin with admin as
    `leave_manager_id` so admin has authority to approve the request.

We DO NOT pre-create the leave request — the agent must create it, confirm it,
then approve it via the manager dashboard.
"""


LEAVE_TYPE_NAME = "Sick Leave"
EMPLOYEE_NAME = "Bench Sick Employee"
EMPLOYEE_LOGIN = "bench_sick_employee"

# The description used for matching the leave record in check.py / state diff.
# The agent's prompt asks them to fill a `Sick leave benchmark` description,
# but Odoo auto-derives hr.leave.name from the type if left blank. We match
# by (employee, type, dates) in check.py to be robust.


def _drop_prior_records(env):
    """Remove any sick leaves for our employee left over from prior runs."""
    user = env["res.users"].search([("login", "=", EMPLOYEE_LOGIN)], limit=1)
    if not user:
        return
    employee = env["hr.employee"].search([("user_id", "=", user.id)], limit=1)
    if not employee:
        return
    prior_leaves = env["hr.leave"].with_context(active_test=False).search([
        ("employee_id", "=", employee.id),
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


def setup(env):
    admin = env.ref("base.user_admin")

    # Grant admin the Time Off Administrator groups so they can approve anyone
    # (belt-and-braces — the base snapshot usually has these already).
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    # Ensure admin has an employee record so the subordinate employee can
    # point at it via parent_id.
    admin_emp = env["hr.employee"].search([("user_id", "=", admin.id)], limit=1)
    if not admin_emp:
        admin_emp = env["hr.employee"].create({
            "name": admin.name or "Administrator",
            "user_id": admin.id,
        })

    # Create / reset the Sick Leave leave type. In this Odoo 19 build
    # `requires_allocation` is a Boolean (default=True). We want sick
    # days bookable WITHOUT a pre-approved allocation, so set it to False.
    # leave_validation_type='hr' => manager must Approve (state: draft ->
    # confirm -> validate) — no intermediate validate1 step.
    leave_type = env["hr.leave.type"].search(
        [("name", "=", LEAVE_TYPE_NAME)], limit=1
    )
    type_vals = {
        "name": LEAVE_TYPE_NAME,
        "requires_allocation": False,
        "leave_validation_type": "hr",
        "request_unit": "day",
        "time_type": "leave",
    }
    if leave_type:
        leave_type.write(type_vals)
    else:
        leave_type = env["hr.leave.type"].create(type_vals)

    # Bench Sick Employee user + employee, admin as reporting & approval
    # manager so our admin session can approve the request.
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

    # Drop any prior leftover leaves for this employee so the agent creates
    # the request from scratch.
    _drop_prior_records(env)
