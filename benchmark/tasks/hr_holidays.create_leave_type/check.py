"""Postcondition checks for hr_holidays.create_leave_type."""

TYPE_NAME = "Conference Attendance"


def check(env):
    failures = []
    types = env["hr.leave.type"].with_context(active_test=False).search([
        ("name", "=", TYPE_NAME),
    ])
    if not types:
        return [f"No leave type found named '{TYPE_NAME}'"]
    if len(types) > 1:
        failures.append(f"Found {len(types)} leave types, expected 1")
    t = types[0]
    if t.leave_validation_type != "manager":
        failures.append(
            f"leave_validation_type is '{t.leave_validation_type}', "
            f"expected 'manager'"
        )
    return failures
