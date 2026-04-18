"""Seed for hr_holidays.bulk_approve_two_pending_requests.

HARD (tier 3): Agent must select exactly two of three pending leaves in the
list view and approve them via the bulk selection-actions Approve button.

We seed:
  - Three pending ('confirm') leaves: Alice (distractor — keep pending),
    Eve (approve), Frank (approve).
  - One already-validated distractor leave (must stay 'validate').
  - One already-refused distractor leave (must stay 'refuse').

Alice's pending leave is the calibration trap: if the agent just "select-all
+ approve", Alice's leave flips to 'validate' and the check fails.
"""


LEAVE_EVE = "Family vacation"
LEAVE_FRANK = "Wedding attendance"
LEAVE_ALICE = "Personal errands"
LEAVE_DONE = "Already approved holiday"
LEAVE_REFUSED = "Already refused day"

EMP_EVE = "Eve Pending"
EMP_FRANK = "Frank Pending"
EMP_ALICE = "Alice Pending"
EMP_DONE = "Diana Done"
EMP_REFUSED = "Robert Refused"

LEAVE_TYPE = "Paid Time Off"


def _ensure_user_employee(env, name, login):
    user = env["res.users"].search([("login", "=", login)], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": name,
            "login": login,
            "password": login,
            "group_ids": [(4, env.ref("base.group_user").id)],
        })
    # Rename existing user to our canonical display name (handles reuse)
    if user.name != name:
        user.sudo().write({"name": name})
    employee = env["hr.employee"].search([("user_id", "=", user.id)], limit=1)
    if not employee:
        employee = env["hr.employee"].create({
            "name": name,
            "user_id": user.id,
        })
    elif employee.name != name:
        employee.sudo().write({"name": name})
    return user, employee


def _drop_prior(env, leave_names):
    prior = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", list(leave_names)),
    ])
    for l in prior:
        try:
            if l.state == "validate":
                l.action_refuse()
                l.action_draft()
            elif l.state in ("confirm", "validate1", "refuse"):
                l.action_draft()
        except Exception:
            pass
    prior.unlink()


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

    # Cleanup prior runs.
    _drop_prior(env, [
        LEAVE_EVE, LEAVE_FRANK, LEAVE_ALICE, LEAVE_DONE, LEAVE_REFUSED,
    ])

    # Leave type: "Paid Time Off" with manager validation.
    ptype = env["hr.leave.type"].search([("name", "=", LEAVE_TYPE)], limit=1)
    if not ptype:
        ptype = env["hr.leave.type"].create({
            "name": LEAVE_TYPE,
            "requires_allocation": False,
            "leave_validation_type": "manager",
            "request_unit": "day",
        })
    else:
        ptype.write({
            "requires_allocation": False,
            "leave_validation_type": "manager",
            "request_unit": "day",
        })

    # Employees/users for all 5 leaves.
    eve_user, eve_emp = _ensure_user_employee(env, EMP_EVE, "eve_pending")
    frank_user, frank_emp = _ensure_user_employee(env, EMP_FRANK, "frank_pending")
    alice_user, alice_emp = _ensure_user_employee(env, EMP_ALICE, "alice_pending")
    diana_user, diana_emp = _ensure_user_employee(env, EMP_DONE, "diana_done")
    robert_user, robert_emp = _ensure_user_employee(env, EMP_REFUSED, "robert_refused")

    # Every employee's leave manager is admin so admin can approve.
    for emp in [eve_emp, frank_emp, alice_emp, diana_emp, robert_emp]:
        emp.write({"leave_manager_id": admin.id})

    def _create_leave(emp_user, emp, name, date_from, date_to):
        leave = env["hr.leave"].with_user(emp_user).create({
            "name": name,
            "holiday_status_id": ptype.id,
            "employee_id": emp.id,
            "request_date_from": date_from,
            "request_date_to": date_to,
        })
        if leave.state == "draft":
            leave.action_confirm()
        return leave

    # Three pending (confirm state) leaves.
    _create_leave(eve_user, eve_emp, LEAVE_EVE, "2026-05-04", "2026-05-06")
    _create_leave(frank_user, frank_emp, LEAVE_FRANK, "2026-05-11", "2026-05-13")
    _create_leave(alice_user, alice_emp, LEAVE_ALICE, "2026-05-18", "2026-05-20")

    # Distractor: already-approved leave (validate). Keep at 'validate'.
    done_leave = _create_leave(
        diana_user, diana_emp, LEAVE_DONE, "2026-04-06", "2026-04-07",
    )
    # Approve as admin (leave manager) to flip to validate.
    done_leave.with_user(admin).action_approve()

    # Distractor: already-refused leave. Keep at 'refuse'.
    refused_leave = _create_leave(
        robert_user, robert_emp, LEAVE_REFUSED, "2026-04-13", "2026-04-14",
    )
    refused_leave.with_user(admin).action_refuse()
