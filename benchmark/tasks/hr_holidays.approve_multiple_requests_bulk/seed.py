"""Seed for hr_holidays.approve_multiple_requests_bulk.

HARD (tier 3): Agent must bulk-approve three pending ('confirm') leave
requests from the Time Off manager list view, while a fourth request
from Bench Diana must remain in state='refuse' (already refused — not
to be re-approved).

We seed four bench employees plus their leave requests:
  - Bench Alice — 2-day Paid Time Off — confirm (To Approve)
  - Bench Bob   — 3-day Paid Time Off — confirm (To Approve)
  - Bench Carol — 1-day Paid Time Off — confirm (To Approve)
  - Bench Diana — 1-day Paid Time Off — refuse (distractor, already refused;
    must stay refused, must NOT be re-approved)

Odoo 19's hr.leave has no 'draft' state — the default on create is
'confirm'. The closest analogue to a non-actionable request is a
refused leave, which is listed in the manager dashboard but not
eligible for bulk approval. Selecting Diana's refused row and hitting
Approve must NOT flip her to 'validate'.

The leave type uses `leave_validation_type='hr'` (HR Officer single-step
validation) so `action_approve` transitions straight from 'confirm' to
'validate' rather than to 'validate1' (double validation).
"""


BENCH_EMPLOYEES = [
    # (display_name, login, leave_name, days, date_from, date_to, post_state)
    # post_state: 'confirm' (pending, keep in confirm) | 'refuse' (refuse after confirm)
    ("Bench Alice", "bench_alice", "Bench Alice vacation", 2,
     "2026-06-01", "2026-06-02", "confirm"),
    ("Bench Bob", "bench_bob", "Bench Bob vacation", 3,
     "2026-06-08", "2026-06-10", "confirm"),
    ("Bench Carol", "bench_carol", "Bench Carol vacation", 1,
     "2026-06-15", "2026-06-15", "confirm"),
    ("Bench Diana", "bench_diana", "Bench Diana vacation", 1,
     "2026-06-22", "2026-06-22", "refuse"),  # distractor — already refused
]

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

    # Grant admin Time Off administrator/officer groups so they can
    # approve anyone's leave from the manager list.
    for grp_ref in [
        "hr_holidays.group_hr_holidays_user",
        "hr_holidays.group_hr_holidays_manager",
        "hr_holidays.group_hr_holidays_responsible",
    ]:
        g = env.ref(grp_ref, raise_if_not_found=False)
        if g and g not in admin.group_ids:
            admin.write({"group_ids": [(4, g.id)]})

    leave_names = [row[2] for row in BENCH_EMPLOYEES]
    _drop_prior(env, leave_names)

    # Leave type: "Paid Time Off" with HR-officer single-step validation.
    # leave_validation_type='hr' means action_approve goes confirm->validate
    # in ONE step (not confirm->validate1->validate as with 'both').
    ptype = env["hr.leave.type"].search([("name", "=", LEAVE_TYPE)], limit=1)
    if not ptype:
        ptype = env["hr.leave.type"].create({
            "name": LEAVE_TYPE,
            "requires_allocation": False,
            "leave_validation_type": "hr",
            "request_unit": "day",
        })
    else:
        ptype.write({
            "requires_allocation": False,
            "leave_validation_type": "hr",
            "request_unit": "day",
        })

    # Create four bench employees and their leave requests.
    for (name, login, leave_name, days, date_from, date_to,
         post_state) in BENCH_EMPLOYEES:
        emp_user, emp = _ensure_user_employee(env, name, login)
        # Admin is every bench employee's leave manager so admin sees
        # them in the Waiting For Me facet and can approve.
        emp.write({"leave_manager_id": admin.id})

        leave = env["hr.leave"].with_user(emp_user).create({
            "name": leave_name,
            "holiday_status_id": ptype.id,
            "employee_id": emp.id,
            "request_date_from": date_from,
            "request_date_to": date_to,
        })

        # In Odoo 19, default state on create is 'confirm' (To Approve).
        # For Diana, refuse the leave so it sits at state='refuse'
        # (a distractor — not eligible for re-approval).
        if post_state == "refuse":
            leave.with_user(admin).action_refuse()
