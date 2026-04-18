"""Cleanup for maintenance.schedule_preventive_plan_recurring."""


def cleanup(env):
    env["maintenance.request"].with_context(active_test=False).search([
        ("name", "=", "Monthly Belt Inspection"),
    ]).unlink()
    env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Conveyor Belt CB-7"),
    ]).unlink()
