"""Postcondition checks for hr_holidays.allocate_sick_leave_to_employee.

Validates:
1. A validated allocation with name '2026 Sick leave pool' exists.
2. Employee is Marc Demo.
3. Leave type is Sick Time Off.
4. number_of_days is exactly 15.
5. State is 'validate' (Approved).
"""


def check(env):
    failures = []

    allocs = env["hr.leave.allocation"].with_context(active_test=False).search([
        ("name", "=", "2026 Sick leave pool"),
    ])
    if not allocs:
        return ["No allocation found with description '2026 Sick leave pool'"]
    if len(allocs) > 1:
        failures.append(f"Found {len(allocs)} allocations, expected exactly 1")

    alloc = allocs[0]

    if alloc.state != "validate":
        failures.append(
            f"Allocation state is '{alloc.state}', expected 'validate' (Approved)"
        )

    if alloc.employee_id.name != "Marc Demo":
        failures.append(
            f"Allocation employee is '{alloc.employee_id.name}', expected 'Marc Demo'"
        )

    if alloc.holiday_status_id.name != "Sick Time Off":
        failures.append(
            f"Allocation leave type is '{alloc.holiday_status_id.name}', "
            f"expected 'Sick Time Off'"
        )

    if abs(alloc.number_of_days - 15.0) > 1e-6:
        failures.append(
            f"Allocation number_of_days is {alloc.number_of_days}, expected 15"
        )

    return failures
