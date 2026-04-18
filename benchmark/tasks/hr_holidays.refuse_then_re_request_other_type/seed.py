"""Seed for hr_holidays.refuse_then_re_request_other_type.

Sets up a confirmed Paid Time Off request from Eve Employee that the
admin (acting as her leave manager) must refuse, then expects the
admin to create a brand-new Sick Time Off request on Eve's behalf for
the same dates.
"""


ORIGINAL_LEAVE_NAME = "Family vacation"
NEW_LEAVE_NAME = "Sick leave per manager"
EVE_LOGIN = "eve_employee_bench"
EVE_NAME = "Eve Employee"
PAID_TYPE = "Paid Time Off"
SICK_TYPE = "Sick Time Off"


def setup(env):
    # 1. Cleanup prior runs (any leftover leaves under either description).
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", [ORIGINAL_LEAVE_NAME, NEW_LEAVE_NAME]),
    ])
    for leave in prior:
        if leave.state == "validate":
            leave.action_refuse()
            leave.action_draft()
        elif leave.state in ("confirm", "validate1", "refuse"):
            leave.action_draft()
    prior.unlink()

    # 2. Ensure admin holds the manager + responsible groups.
    admin = env.ref("base.user_admin")
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        group = env.ref(grp_ref, raise_if_not_found=False)
        if group and group not in admin.group_ids:
            admin.write({"group_ids": [(4, group.id)]})

    # 3. Ensure Eve Employee user + employee record exists with admin as
    #    her leave manager.
    eve_user = env["res.users"].search([("login", "=", EVE_LOGIN)], limit=1)
    if not eve_user:
        eve_user = env["res.users"].create({
            "name": EVE_NAME,
            "login": EVE_LOGIN,
            "password": EVE_LOGIN,
            "group_ids": [(4, env.ref("base.group_user").id)],
        })
    else:
        eve_user.write({"name": EVE_NAME})

    eve_employee = env["hr.employee"].search(
        [("user_id", "=", eve_user.id)], limit=1
    )
    if not eve_employee:
        eve_employee = env["hr.employee"].create({
            "name": EVE_NAME,
            "user_id": eve_user.id,
        })
    else:
        eve_employee.write({"name": EVE_NAME})
    eve_employee.write({"leave_manager_id": admin.id})

    # 4. Ensure Paid Time Off and Sick Time Off leave types exist with
    #    sane validation settings (manager only, no allocation needed).
    paid = env["hr.leave.type"].search([("name", "=", PAID_TYPE)], limit=1)
    if not paid:
        paid = env["hr.leave.type"].create({
            "name": PAID_TYPE,
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })
    else:
        paid.write({
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })

    sick = env["hr.leave.type"].search([("name", "=", SICK_TYPE)], limit=1)
    if not sick:
        sick = env["hr.leave.type"].create({
            "name": SICK_TYPE,
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })
    else:
        sick.write({
            "requires_allocation": False,
            "leave_validation_type": "manager",
        })

    # 5. Submit the original Paid Time Off request as Eve so it lands in
    #    'confirm' (To Approve) state, ready for admin to refuse.
    leave = env["hr.leave"].with_user(eve_user).create({
        "name": ORIGINAL_LEAVE_NAME,
        "holiday_status_id": paid.id,
        "employee_id": eve_employee.id,
        "request_date_from": "2026-08-10",
        "request_date_to": "2026-08-12",
    })
    if leave.state == "draft":
        leave.action_confirm()
