"""Cleanup for maintenance.create_equipment_assign_category_team."""


def cleanup(env):
    env["maintenance.equipment"].with_context(active_test=False).search([
        "|",
        ("name", "=", "Dock Scanner DS-200"),
        ("serial_no", "=", "DS-200-SN-1042"),
    ]).unlink()
