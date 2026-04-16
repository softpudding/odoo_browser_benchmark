"""Postcondition checks for hr.assign_manager_set_work_location."""


def check(env):
    failures = []

    emp = env["hr.employee"].search([("name", "=", "Maya Ortiz")], limit=1)
    if not emp:
        return ["Employee 'Maya Ortiz' not found"]

    if emp.parent_id.name != "Nadia Reyes":
        failures.append(f"Manager is '{emp.parent_id.name}', expected 'Nadia Reyes'")
    if not emp.work_location_id or emp.work_location_id.name != "HQ Annex":
        failures.append(
            f"Work location is '{emp.work_location_id.name if emp.work_location_id else None}', expected 'HQ Annex'"
        )
    if emp.work_phone != "+1 555 0450":
        failures.append(f"Work phone is '{emp.work_phone}', expected '+1 555 0450'")
    if emp.job_id.name != "Operations Coordinator":
        failures.append(
            f"Job changed to '{emp.job_id.name}', expected 'Operations Coordinator'"
        )
    if emp.department_id.name != "Operations":
        failures.append(
            f"Department changed to '{emp.department_id.name}', expected 'Operations'"
        )

    return failures
