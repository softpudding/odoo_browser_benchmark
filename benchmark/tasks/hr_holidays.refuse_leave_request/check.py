"""Postcondition checks for hr_holidays.refuse_leave_request."""


LEAVE_NAME = "Unscheduled absence — please refuse"


def check(env):
    failures = []
    leaves = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", LEAVE_NAME),
    ])
    if not leaves:
        return [f"No leave found named '{LEAVE_NAME}'"]
    if len(leaves) > 1:
        failures.append(f"Found {len(leaves)} leaves, expected 1")
    if leaves[0].state != "refuse":
        failures.append(
            f"Leave state is '{leaves[0].state}', expected 'refuse'"
        )
    return failures
