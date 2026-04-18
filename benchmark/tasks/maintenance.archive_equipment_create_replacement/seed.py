"""Seed for maintenance.archive_equipment_create_replacement.

Ensures the 'Warehouse Gear' equipment category exists, creates the active
'Old Belt OB-99' equipment in that category, and removes any prior
'New Belt NB-100' record (or leftovers of the old belt) from a previous run.
"""


def setup(env):
    # Ensure the equipment category exists.
    category = env["maintenance.equipment.category"].search(
        [("name", "=", "Warehouse Gear")], limit=1
    )
    if not category:
        category = env["maintenance.equipment.category"].create(
            {"name": "Warehouse Gear"}
        )

    # Cleanup: remove any prior runs' equipment records (active or archived,
    # by name or by the expected serial numbers — serial_no is unique).
    env["maintenance.equipment"].with_context(active_test=False).search([
        "|", "|", "|",
        ("name", "=", "Old Belt OB-99"),
        ("name", "=", "New Belt NB-100"),
        ("serial_no", "=", "OB-99-SN-2019"),
        ("serial_no", "=", "NB-100-SN-2026"),
    ]).unlink()

    # Create the seeded 'Old Belt OB-99' active in 'Warehouse Gear'.
    env["maintenance.equipment"].create({
        "name": "Old Belt OB-99",
        "serial_no": "OB-99-SN-2019",
        "category_id": category.id,
    })
