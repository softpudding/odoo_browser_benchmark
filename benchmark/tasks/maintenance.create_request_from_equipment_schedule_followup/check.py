"""Postcondition checks for maintenance.create_request_from_equipment_schedule_followup."""


REQUEST_NAME = "Inspect Forklift Battery Cooling"
EQUIPMENT_NAME = "Forklift FL-88"
TEAM_NAME = "Bench Maintenance"
TECHNICIAN_NAME = "Marc Demo"
ACTIVITY_SUMMARY = "Review cooling test report"
ACTIVITY_DATE = "2026-05-23"


def check(env):
    failures = []

    request = env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", REQUEST_NAME),
    ], limit=1)
    if not request:
        return [f"Maintenance request {REQUEST_NAME!r} not found"]

    if request.equipment_id.name != EQUIPMENT_NAME:
        failures.append(
            f"Equipment is {request.equipment_id.name!r}, expected {EQUIPMENT_NAME!r}"
        )
    if request.maintenance_team_id.name != TEAM_NAME:
        failures.append(
            f"Maintenance team is {request.maintenance_team_id.name!r}, expected {TEAM_NAME!r}"
        )
    if request.user_id.name != TECHNICIAN_NAME:
        failures.append(
            f"Technician is {request.user_id.name!r}, expected {TECHNICIAN_NAME!r}"
        )
    if request.stage_id and request.stage_id.done:
        failures.append(
            f"Stage is {request.stage_id.name!r}, expected a non-done stage"
        )

    activity = env["mail.activity"].search([
        ("res_model", "=", "maintenance.request"),
        ("res_id", "=", request.id),
        ("summary", "=", ACTIVITY_SUMMARY),
    ], limit=1)
    if not activity:
        failures.append(f"Follow-up activity {ACTIVITY_SUMMARY!r} not found on the request")
    else:
        if str(activity.date_deadline) != ACTIVITY_DATE:
            failures.append(
                f"Activity deadline is {activity.date_deadline!s}, expected {ACTIVITY_DATE}"
            )

    return failures
