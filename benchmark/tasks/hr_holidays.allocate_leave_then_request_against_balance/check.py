"""Postcondition checks for hr_holidays.allocate_leave_then_request_against_balance."""

from datetime import date


def check(env):
    failures = []

    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", "Quarter-End Sick Leave Buffer"),
    ])
    if not allocs:
        return ["No allocation found with description 'Quarter-End Sick Leave Buffer'"]
    if len(allocs) > 1:
        failures.append(f"Found {len(allocs)} allocations, expected exactly 1")

    alloc = allocs[0]
    if alloc.state != "validate":
        failures.append(f"Allocation state is '{alloc.state}', expected 'validate'")
    if alloc.employee_id.name != "Marc Demo":
        failures.append(f"Allocation employee is '{alloc.employee_id.name}', expected 'Marc Demo'")
    if alloc.holiday_status_id.name != "Sick Time Off":
        failures.append(f"Allocation leave type is '{alloc.holiday_status_id.name}', expected 'Sick Time Off'")
    if abs(alloc.number_of_days - 4.0) > 1e-6:
        failures.append(f"Allocation number_of_days is {alloc.number_of_days}, expected 4")

    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Warehouse flu recovery"),
    ])
    if not leaves:
        failures.append("No leave request found with description 'Warehouse flu recovery'")
        return failures
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} leave requests, expected exactly 1")

    leave = leaves[0]
    if leave.state != "validate":
        failures.append(f"Leave state is '{leave.state}', expected 'validate'")
    if leave.employee_id.name != "Marc Demo":
        failures.append(f"Leave employee is '{leave.employee_id.name}', expected 'Marc Demo'")
    if leave.holiday_status_id.name != "Sick Time Off":
        failures.append(f"Leave type is '{leave.holiday_status_id.name}', expected 'Sick Time Off'")
    if leave.request_date_from != date(2026, 6, 23):
        failures.append(f"Leave start date is {leave.request_date_from}, expected 2026-06-23")
    if leave.request_date_to != date(2026, 6, 24):
        failures.append(f"Leave end date is {leave.request_date_to}, expected 2026-06-24")
    if abs(leave.number_of_days - 2.0) > 1e-6:
        failures.append(f"Leave number_of_days is {leave.number_of_days}, expected 2")

    return failures
