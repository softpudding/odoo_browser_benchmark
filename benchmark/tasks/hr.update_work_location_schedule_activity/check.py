"""Postcondition checks for hr.update_work_location_schedule_activity."""

from datetime import date

EMPLOYEE_NAME = "Avery Collins"
ACTIVITY_SUMMARY = "Confirm home office setup"


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", EMPLOYEE_NAME)], limit=1)
    if not employee:
        return [f"Employee '{EMPLOYEE_NAME}' not found"]

    if employee.work_phone != "+1 415 555 0188":
        failures.append(
            f"Work Phone is '{employee.work_phone}', expected '+1 415 555 0188'"
        )
    if not employee.work_location_id or employee.work_location_id.name != "Home":
        actual = employee.work_location_id.name if employee.work_location_id else None
        failures.append(f"Work Location is '{actual}', expected 'Home'")
    if employee.job_id and employee.job_id.name != "Customer Success Manager":
        failures.append(
            f"Job Position changed to '{employee.job_id.name}', expected 'Customer Success Manager'"
        )
    if employee.department_id and employee.department_id.name != "Customer Success":
        failures.append(
            f"Department changed to '{employee.department_id.name}', expected 'Customer Success'"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.employee"),
        ("res_id", "=", employee.id),
        ("summary", "=", ACTIVITY_SUMMARY),
    ])
    if len(activities) != 1:
        failures.append(
            f"Expected exactly 1 activity named '{ACTIVITY_SUMMARY}', found {len(activities)}"
        )
    elif activities[0].activity_type_id.name != "Call":
        failures.append(
            f"Activity type is '{activities[0].activity_type_id.name}', expected 'Call'"
        )
    elif activities[0].date_deadline != date(2026, 5, 19):
        failures.append(
            f"Activity due date is {activities[0].date_deadline}, expected 2026-05-19"
        )

    return failures
