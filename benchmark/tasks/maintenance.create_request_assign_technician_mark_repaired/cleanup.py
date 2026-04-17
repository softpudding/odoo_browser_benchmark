"""Cleanup for maintenance.create_request_assign_technician_mark_repaired."""


def cleanup(env):
    env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Replace Dock Sensor"),
    ]).unlink()
    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Forklift FL-88"),
    ]).unlink()
