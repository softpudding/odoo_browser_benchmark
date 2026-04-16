"""Postcondition checks for hr.create_employee_complete_profile.

Validates that the employee was created with the correct main-form fields,
Work Information tab fields, and Private Information tab fields.
"""


def check(env):
    failures = []

    employee = env["hr.employee"].search([("name", "=", "Jordan Mercer")], limit=1)
    if not employee:
        return ["Employee 'Jordan Mercer' not found"]

    # --- Main form checks ---
    if not employee.job_id or employee.job_id.name != "Field Operations Coordinator":
        actual = employee.job_id.name if employee.job_id else "(none)"
        failures.append(
            f"Job Position: expected 'Field Operations Coordinator', got '{actual}'"
        )

    if employee.work_phone != "+1 (555) 840-2200":
        failures.append(
            f"Work Phone: expected '+1 (555) 840-2200', got '{employee.work_phone}'"
        )

    # --- Work Information tab checks ---
    if not employee.work_location_id or employee.work_location_id.name != "Home":
        actual = employee.work_location_id.name if employee.work_location_id else "(none)"
        failures.append(
            f"Work Location: expected 'Home', got '{actual}'"
        )

    if not employee.resource_calendar_id or "40" not in employee.resource_calendar_id.name:
        actual = employee.resource_calendar_id.name if employee.resource_calendar_id else "(none)"
        failures.append(
            f"Working Hours: expected schedule containing '40', got '{actual}'"
        )

    # --- Private Information tab checks ---
    if employee.certificate != "bachelor":
        actual = employee.certificate or "(none)"
        failures.append(
            f"Certificate Level: expected 'bachelor', got '{actual}'"
        )

    if employee.marital != "single":
        actual = employee.marital or "(none)"
        failures.append(
            f"Marital Status: expected 'single', got '{actual}'"
        )

    return failures
