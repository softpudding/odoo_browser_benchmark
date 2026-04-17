"""Postcondition checks for hr_holidays.request_time_off_approve.

Validates:
1. A time-off request exists with name "Medical appointment recovery".
2. It uses the "Sick Time Off" leave type.
3. Dates are June 9-11, 2026.
4. State is "validate" (approved).
"""

from datetime import date


def check(env):
    failures = []

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Medical appointment recovery"),
    ])
    if not leaves:
        return ["No time-off request found with description 'Medical appointment recovery'"]
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} requests, expected exactly 1")

    leave = leaves[0]

    if leave.state != "validate":
        failures.append(f"Leave state is '{leave.state}', expected 'validate'")

    if leave.holiday_status_id.name != "Sick Time Off":
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', expected 'Sick Time Off'"
        )

    # Check dates (date_from/date_to are datetimes, compare date part)
    from_date = leave.date_from.date() if leave.date_from else None
    to_date = leave.date_to.date() if leave.date_to else None

    if from_date != date(2026, 6, 9):
        failures.append(f"Start date is {from_date}, expected 2026-06-09")
    # to_date may be end of day June 11
    if to_date and to_date != date(2026, 6, 11):
        failures.append(f"End date is {to_date}, expected 2026-06-11")

    return failures
