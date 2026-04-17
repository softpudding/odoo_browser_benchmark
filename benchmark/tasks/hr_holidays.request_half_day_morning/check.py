"""Postcondition checks for hr_holidays.request_half_day_morning."""

from datetime import date


def check(env):
    failures = []

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Doctor appointment"),
    ])
    if not leaves:
        return ["No time-off request found with description 'Doctor appointment'"]
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} requests, expected exactly 1")

    leave = leaves[0]

    if leave.state not in ("confirm", "validate1"):
        failures.append(
            f"Leave state is '{leave.state}', expected 'confirm' (To Approve)"
        )

    if leave.holiday_status_id.name != "Paid Time Off":
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', expected 'Paid Time Off'"
        )

    if not leave.request_unit_half:
        failures.append(
            "Half Day toggle is off — expected request_unit_half=True"
        )

    if leave.request_date_from_period != "am":
        failures.append(
            f"Period is '{leave.request_date_from_period}', expected 'am' (Morning)"
        )

    if abs(leave.number_of_days - 0.5) > 1e-6:
        failures.append(
            f"number_of_days is {leave.number_of_days}, expected 0.5 (half day)"
        )

    req_from = leave.request_date_from
    if req_from != date(2026, 6, 15):
        failures.append(f"Date is {req_from}, expected 2026-06-15")

    return failures
