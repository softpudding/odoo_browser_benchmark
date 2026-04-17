"""Postcondition checks for hr_holidays.request_annual_leave."""

from datetime import date


def check(env):
    failures = []

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Family vacation to Iceland"),
    ])
    if not leaves:
        return ["No leave request found with description 'Family vacation to Iceland'"]
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} requests, expected exactly 1")

    leave = leaves[0]

    if leave.state not in ("confirm", "validate1", "validate"):
        failures.append(
            f"Leave state is '{leave.state}', expected 'confirm' (To Approve)"
        )
    if leave.state == "validate":
        failures.append("Leave should not be approved; leave it in To Approve state")

    if leave.holiday_status_id.name != "Paid Time Off":
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', expected 'Paid Time Off'"
        )

    from_date = leave.date_from.date() if leave.date_from else None
    to_date = leave.date_to.date() if leave.date_to else None
    if from_date != date(2026, 7, 20):
        failures.append(f"Start date is {from_date}, expected 2026-07-20")
    if to_date and to_date != date(2026, 7, 22):
        failures.append(f"End date is {to_date}, expected 2026-07-22")

    if abs(leave.number_of_days - 3.0) > 0.01:
        failures.append(
            f"number_of_days is {leave.number_of_days}, expected 3.0"
        )

    admin = env.ref("base.user_admin")
    admin_employee = env["hr.employee"].search(
        [("user_id", "=", admin.id)], limit=1
    )
    if admin_employee and leave.employee_id != admin_employee:
        failures.append(
            f"Leave employee is '{leave.employee_id.name}', expected admin's employee"
        )

    return failures
