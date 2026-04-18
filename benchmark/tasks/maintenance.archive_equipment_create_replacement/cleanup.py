"""Cleanup for maintenance.archive_equipment_create_replacement."""


def cleanup(env):
    env["maintenance.equipment"].with_context(active_test=False).search([
        "|", "|", "|",
        ("name", "=", "Old Belt OB-99"),
        ("name", "=", "New Belt NB-100"),
        ("serial_no", "=", "OB-99-SN-2019"),
        ("serial_no", "=", "NB-100-SN-2026"),
    ]).unlink()
