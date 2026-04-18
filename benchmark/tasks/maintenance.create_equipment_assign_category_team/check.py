"""Postcondition checks for maintenance.create_equipment_assign_category_team."""


def check(env):
    failures = []

    equipment = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Dock Scanner DS-200"),
    ])
    if not equipment:
        return ["Equipment 'Dock Scanner DS-200' not found"]
    if len(equipment) > 1:
        failures.append(
            f"Expected exactly 1 equipment named 'Dock Scanner DS-200', found {len(equipment)}"
        )
    equipment = equipment[0]

    if not equipment.active:
        failures.append("Equipment is archived; expected it to remain active")

    if equipment.serial_no != "DS-200-SN-1042":
        failures.append(
            f"Serial number is {equipment.serial_no!r}, expected 'DS-200-SN-1042'"
        )

    if not equipment.category_id or equipment.category_id.name != "Warehouse Gear":
        failures.append(
            f"Category is {equipment.category_id.name!r}, expected 'Warehouse Gear'"
        )

    if (
        not equipment.maintenance_team_id
        or equipment.maintenance_team_id.name != "Bench Maintenance"
    ):
        failures.append(
            f"Team is {equipment.maintenance_team_id.name!r}, expected 'Bench Maintenance'"
        )

    return failures
