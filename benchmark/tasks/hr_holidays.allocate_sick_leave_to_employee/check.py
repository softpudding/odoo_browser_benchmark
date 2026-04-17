"""Postcondition checks for hr_holidays.allocate_sick_leave_to_employee."""


EMPLOYEE_NAME = "Benchmark Allocatee"
USER_LOGIN = "benchmark_allocatee"


def check(env):
    failures = []

    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", USER_LOGIN)], limit=1
    )
    employee = None
    if user:
        employee = env["hr.employee"].with_context(active_test=False).search(
            [("user_id", "=", user.id)], limit=1
        )
    if not employee:
        employee = env["hr.employee"].with_context(active_test=False).search(
            [("name", "=", EMPLOYEE_NAME)], limit=1
        )

    if not employee:
        return [f"No hr.employee found for '{EMPLOYEE_NAME}'"]

    allocations = env["hr.leave.allocation"].with_context(
        active_test=False
    ).search([
        ("employee_id", "=", employee.id),
    ])

    if not allocations:
        return [f"No hr.leave.allocation found for employee '{EMPLOYEE_NAME}'"]
    if len(allocations) > 1:
        failures.append(
            f"Found {len(allocations)} allocations for '{EMPLOYEE_NAME}', expected exactly 1"
        )

    alloc = allocations[0]

    leave_type_name = alloc.holiday_status_id.name or ""
    if "Sick" not in leave_type_name:
        failures.append(
            f"Leave type is '{leave_type_name}', expected one containing 'Sick' (e.g. 'Sick Time Off')"
        )

    if abs(alloc.number_of_days - 15.0) > 0.01:
        failures.append(
            f"number_of_days is {alloc.number_of_days}, expected 15.0"
        )

    if alloc.state != "validate":
        failures.append(
            f"Allocation state is '{alloc.state}', expected 'validate' (Approved)"
        )

    return failures
