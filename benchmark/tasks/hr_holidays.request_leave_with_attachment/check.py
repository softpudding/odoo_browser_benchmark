"""Postcondition checks for hr_holidays.request_leave_with_attachment."""

from datetime import date


LEAVE_NAME = "Family event"
LEAVE_TYPE = "Annual Leave"
EXPECTED_FROM = date(2026, 3, 9)
EXPECTED_TO = date(2026, 3, 10)
EXPECTED_DAYS = 2.0


def check(env):
    failures = []

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    if not leaves:
        return [f"No leave request found with description {LEAVE_NAME!r}"]
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} requests, expected exactly 1")

    leave = leaves[0]

    if leave.state not in ("confirm", "validate1", "validate"):
        failures.append(
            f"Leave state is '{leave.state}', expected 'confirm' (To Approve)"
        )
    if leave.state == "validate":
        failures.append(
            "Leave should not be approved; leave it in To Approve state"
        )

    if leave.holiday_status_id.name != LEAVE_TYPE:
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', "
            f"expected '{LEAVE_TYPE}'"
        )

    from_date = leave.date_from.date() if leave.date_from else None
    to_date = leave.date_to.date() if leave.date_to else None
    if from_date != EXPECTED_FROM:
        failures.append(f"Start date is {from_date}, expected {EXPECTED_FROM}")
    if to_date and to_date != EXPECTED_TO:
        failures.append(f"End date is {to_date}, expected {EXPECTED_TO}")

    if abs(leave.number_of_days - EXPECTED_DAYS) > 0.01:
        failures.append(
            f"number_of_days is {leave.number_of_days}, expected {EXPECTED_DAYS}"
        )

    admin = env.ref("base.user_admin")
    admin_employee = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if admin_employee and leave.employee_id != admin_employee:
        failures.append(
            f"Leave employee is '{leave.employee_id.name}', "
            f"expected admin's employee"
        )

    # Attachment: at least one ir.attachment linked to this hr.leave.
    attachments = env["ir.attachment"].search([
        ("res_model", "=", "hr.leave"),
        ("res_id", "=", leave.id),
    ])
    if len(attachments) == 0:
        failures.append(
            f"No ir.attachment linked to hr.leave id={leave.id} "
            f"(res_model='hr.leave'); the PDF justification was not attached "
            f"via the chatter"
        )
    else:
        has_nonempty = any(
            (att.datas or att.raw) for att in attachments
        )
        if not has_nonempty:
            failures.append(
                "All attachments linked to this leave are empty"
            )

    return failures
