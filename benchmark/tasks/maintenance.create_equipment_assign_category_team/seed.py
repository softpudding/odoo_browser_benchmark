"""Seed for maintenance.create_equipment_assign_category_team.

Ensures the 'Warehouse Gear' equipment category and 'Bench Maintenance'
maintenance team exist, and removes any prior 'Dock Scanner DS-200'
equipment from a previous run.
"""


def setup(env):
    # Ensure the maintenance team exists.
    team = env["maintenance.team"].search(
        [("name", "=", "Bench Maintenance")], limit=1
    )
    if not team:
        team = env["maintenance.team"].create({"name": "Bench Maintenance"})

    # Ensure the equipment category exists.
    category = env["maintenance.equipment.category"].search(
        [("name", "=", "Warehouse Gear")], limit=1
    )
    if not category:
        category = env["maintenance.equipment.category"].create(
            {"name": "Warehouse Gear"}
        )

    # Cleanup: remove any equipment records from prior runs
    # (match by name or by the expected serial number — serial_no is unique).
    env["maintenance.equipment"].with_context(active_test=False).search([
        "|",
        ("name", "=", "Dock Scanner DS-200"),
        ("serial_no", "=", "DS-200-SN-1042"),
    ]).unlink()
