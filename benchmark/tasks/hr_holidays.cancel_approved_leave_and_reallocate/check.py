"""Postcondition checks for hr_holidays.cancel_approved_leave_and_reallocate."""


def check(env):
    failures = []

    tentative = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Family vacation (tentative)"),
    ])
    if not tentative:
        failures.append(
            "Original 'Family vacation (tentative)' leave was deleted — "
            "it should be refused, not unlinked"
        )
        return failures
    if len(tentative) > 1:
        failures.append(
            f"Found {len(tentative)} tentative leaves, expected 1"
        )
    if tentative[0].state != "refuse":
        failures.append(
            f"Tentative leave state is '{tentative[0].state}', "
            f"expected 'refuse'"
        )

    return failures
