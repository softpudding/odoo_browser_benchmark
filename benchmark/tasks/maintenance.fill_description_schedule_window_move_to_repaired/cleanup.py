"""Cleanup for maintenance.fill_description_schedule_window_move_to_repaired."""

REQUEST_NAME = "Replace Conveyor Drive Belt"
EQUIPMENT_NAME = "Conveyor CV-22"


def cleanup(env):
    env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", REQUEST_NAME),
    ]).unlink()
    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", EQUIPMENT_NAME),
    ]).unlink()
