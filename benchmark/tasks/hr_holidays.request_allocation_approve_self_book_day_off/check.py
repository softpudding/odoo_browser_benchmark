"""Postcondition checks for hr_holidays.request_allocation_approve_self_book_day_off."""

from datetime import date


LEAVE_TYPE_NAME = "Bench Bonus Days"
EMPLOYEE_NAME = "Bench Worker"
ALLOC_DESC = "Q2 bonus"
LEAVE_DESC = "Bench day off"


def check(env):
    failures = []

    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", ALLOC_DESC),
    ])
    if not allocs:
        failures.append(
            f"No allocation found with description '{ALLOC_DESC}'"
        )
    else:
        if len(allocs) > 1:
            failures.append(
                f"Found {len(allocs)} allocations named '{ALLOC_DESC}', expected 1"
            )
        alloc = allocs[0]
        if alloc.state != "validate":
            failures.append(
                f"Allocation state is '{alloc.state}', expected 'validate'"
            )
        if alloc.employee_id.name != EMPLOYEE_NAME:
            failures.append(
                f"Allocation employee is '{alloc.employee_id.name}', "
                f"expected '{EMPLOYEE_NAME}'"
            )
        if alloc.holiday_status_id.name != LEAVE_TYPE_NAME:
            failures.append(
                f"Allocation leave type is '{alloc.holiday_status_id.name}', "
                f"expected '{LEAVE_TYPE_NAME}'"
            )
        if abs(alloc.number_of_days - 5.0) > 1e-6:
            failures.append(
                f"Allocation number_of_days is {alloc.number_of_days}, expected 5"
            )

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_DESC),
    ])
    if not leaves:
        failures.append(
            f"No leave request found with description '{LEAVE_DESC}'"
        )
        return failures
    if len(leaves) > 1:
        failures.append(
            f"Found {len(leaves)} leave requests named '{LEAVE_DESC}', expected 1"
        )

    leave = leaves[0]
    if leave.state != "validate":
        failures.append(
            f"Leave state is '{leave.state}', expected 'validate'"
        )
    if leave.employee_id.name != EMPLOYEE_NAME:
        failures.append(
            f"Leave employee is '{leave.employee_id.name}', "
            f"expected '{EMPLOYEE_NAME}'"
        )
    if leave.holiday_status_id.name != LEAVE_TYPE_NAME:
        failures.append(
            f"Leave type is '{leave.holiday_status_id.name}', "
            f"expected '{LEAVE_TYPE_NAME}'"
        )
    if leave.request_date_from != date(2026, 5, 15):
        failures.append(
            f"Leave start date is {leave.request_date_from}, expected 2026-05-15"
        )
    if leave.request_date_to != date(2026, 5, 15):
        failures.append(
            f"Leave end date is {leave.request_date_to}, expected 2026-05-15"
        )
    if abs(leave.number_of_days - 1.0) > 1e-6:
        failures.append(
            f"Leave number_of_days is {leave.number_of_days}, expected 1"
        )

    return failures
