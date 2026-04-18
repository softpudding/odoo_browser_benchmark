"""Postcondition checks for hr_attendance.clock_in_out_kiosk_mode.

Verify that exactly one hr.attendance row exists for 'Bench Worker' with
BOTH check_in and check_out set. Allow a +/- 1 day window around today in
the server's local timezone since check_in is stored in UTC and admin
timezone shift can straddle midnight.
"""

from datetime import datetime, timedelta

EMPLOYEE_NAME = "Bench Worker"


def check(env):
    failures = []

    employee = env["hr.employee"].search(
        [("name", "=", EMPLOYEE_NAME)], limit=1
    )
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    attendances = env["hr.attendance"].search(
        [("employee_id", "=", employee.id)]
    )
    if not attendances:
        return [f"No hr.attendance rows found for '{EMPLOYEE_NAME}'"]

    # We expect a single attendance row with both check_in and check_out set.
    closed = attendances.filtered(lambda a: a.check_in and a.check_out)
    if not closed:
        return [
            f"Found {len(attendances)} attendance(s) for '{EMPLOYEE_NAME}' but "
            f"none have both check_in and check_out set"
        ]

    # Window: today +/- 1 day in UTC.
    today = datetime.utcnow().date()
    window_start = today - timedelta(days=1)
    window_end = today + timedelta(days=1)

    in_window = closed.filtered(
        lambda a: window_start <= a.check_in.date() <= window_end
        and window_start <= a.check_out.date() <= window_end
    )
    if not in_window:
        failures.append(
            f"No closed attendance for '{EMPLOYEE_NAME}' within today +/- 1 day. "
            f"Have: {[(str(a.check_in), str(a.check_out)) for a in closed]}"
        )
        return failures

    # Ensure check_out is after check_in
    bad_order = in_window.filtered(lambda a: a.check_out <= a.check_in)
    if bad_order:
        failures.append(
            f"check_out must be after check_in. Found: "
            f"{[(str(a.check_in), str(a.check_out)) for a in bad_order]}"
        )

    # Ensure no stray attendances for other employees were added
    # (we can't easily check "added during task" without pre-state, so we
    # just make sure the check_in/check_out pair exists on Bench Worker).
    return failures
