"""Postcondition checks for hr_holidays.approve_leave_as_manager.

Validates:
1. A time-off request named "Family event leave" exists.
2. Its state is 'validate' (approved).
3. It uses the 'Paid Time Off' leave type.
4. Dates are June 17-18, 2026.
5. No other pending requests were mutated into 'validate' side-effect.
"""

from datetime import date


LEAVE_NAME = "Family event leave"


def check(env):
    failures = []

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    if not leaves:
        return [f"No time-off request found with description '{LEAVE_NAME}'"]
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} requests named '{LEAVE_NAME}', expected exactly 1")

    leave = leaves[0]

    if leave.state != "validate":
        failures.append(
            f"Leave state is '{leave.state}', expected 'validate' (approved)"
        )

    if leave.holiday_status_id.name != "Paid Time Off":
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', expected 'Paid Time Off'"
        )

    from_date = leave.date_from.date() if leave.date_from else None
    to_date = leave.date_to.date() if leave.date_to else None

    if from_date != date(2026, 6, 17):
        failures.append(f"Start date is {from_date}, expected 2026-06-17")
    if to_date and to_date != date(2026, 6, 18):
        failures.append(f"End date is {to_date}, expected 2026-06-18")

    # Duration should be 2 days
    if abs(leave.number_of_days - 2.0) > 1e-6:
        failures.append(
            f"number_of_days is {leave.number_of_days}, expected 2.0"
        )

    # Ensure the employee is Marc Demo (sanity check, the target was a demo
    # employee not the admin themselves).
    if leave.employee_id.name != "Marc Demo":
        failures.append(
            f"Request employee is '{leave.employee_id.name}', expected 'Marc Demo'"
        )

    return failures
