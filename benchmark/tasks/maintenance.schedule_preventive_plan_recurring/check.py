"""Postcondition checks for maintenance.schedule_preventive_plan_recurring."""

from datetime import date


def check(env):
    failures = []

    equipment = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Conveyor Belt CB-7"),
    ], limit=1)
    if not equipment:
        return ["Equipment 'Conveyor Belt CB-7' not found"]

    if equipment.expected_mtbf != 120:
        failures.append(
            f"equipment.expected_mtbf is {equipment.expected_mtbf}, expected 120"
        )

    request = env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Monthly Belt Inspection"),
    ], limit=1)
    if not request:
        return failures + ["Maintenance request 'Monthly Belt Inspection' not found"]

    if not request.equipment_id or request.equipment_id.id != equipment.id:
        failures.append(
            f"request.equipment_id is {request.equipment_id.display_name!r}, expected 'Conveyor Belt CB-7'"
        )
    if request.maintenance_type != "preventive":
        failures.append(
            f"request.maintenance_type is {request.maintenance_type!r}, expected 'preventive'"
        )
    if not request.maintenance_team_id or request.maintenance_team_id.name != "Bench Maintenance":
        failures.append(
            f"request.maintenance_team_id is {request.maintenance_team_id.name!r}, expected 'Bench Maintenance'"
        )
    if not request.schedule_date or request.schedule_date.date() != date(2026, 5, 15):
        failures.append(
            f"request.schedule_date is {request.schedule_date!r}, expected 2026-05-15"
        )

    return failures
