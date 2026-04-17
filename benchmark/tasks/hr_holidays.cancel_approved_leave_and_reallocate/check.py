"""Postcondition checks for hr_holidays.cancel_approved_leave_and_reallocate."""

from datetime import date


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
    else:
        if len(tentative) > 1:
            failures.append(
                f"Found {len(tentative)} tentative leaves, expected 1"
            )
        if tentative[0].state != "refuse":
            failures.append(
                f"Tentative leave state is '{tentative[0].state}', "
                f"expected 'refuse'"
            )

    confirmed = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", "Family vacation (confirmed)"),
    ])
    if not confirmed:
        return failures + [
            "No replacement leave found with description "
            "'Family vacation (confirmed)'"
        ]
    if len(confirmed) > 1:
        failures.append(
            f"Found {len(confirmed)} confirmed leaves, expected 1"
        )
    c = confirmed[0]

    if c.state != "validate":
        failures.append(
            f"Replacement leave state is '{c.state}', expected 'validate' "
            f"(Approved)"
        )
    if c.employee_id.name != "Marc Demo":
        failures.append(
            f"Replacement employee is '{c.employee_id.name}', "
            f"expected 'Marc Demo'"
        )
    if c.holiday_status_id.name != "Paid Time Off":
        failures.append(
            f"Replacement leave type is '{c.holiday_status_id.name}', "
            f"expected 'Paid Time Off'"
        )
    if c.request_date_from != date(2026, 7, 13):
        failures.append(
            f"Replacement start date is {c.request_date_from}, "
            f"expected 2026-07-13"
        )
    if c.request_date_to != date(2026, 7, 17):
        failures.append(
            f"Replacement end date is {c.request_date_to}, "
            f"expected 2026-07-17"
        )

    return failures
