"""Postcondition checks for maintenance.create_request_assign_technician_mark_repaired."""


def check(env):
    failures = []

    request = env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Replace Dock Sensor"),
    ], limit=1)
    if not request:
        return ["Maintenance request 'Replace Dock Sensor' not found"]

    if not request.equipment_id or request.equipment_id.name != "Forklift FL-88":
        failures.append(f"Equipment is {request.equipment_id.name!r}")
    if not request.user_id or request.user_id.name != "Marc Demo":
        failures.append(f"Technician is {request.user_id.name!r}")
    if not request.stage_id or not request.stage_id.done:
        failures.append(f"Stage is {request.stage_id.name!r}, expected a done stage")

    return failures
