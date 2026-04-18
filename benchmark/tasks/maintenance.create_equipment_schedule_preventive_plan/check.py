"""Postcondition checks for maintenance.create_equipment_schedule_preventive_plan."""


EQUIPMENT_NAME = "Bench Press 01"
CATEGORY_NAME = "Machinery"
TECHNICIAN_NAME = "Bench Tech"
EXPECTED_MTBF = 30
EFFECTIVE_DATE = "2026-06-01"


def check(env):
    failures = []

    equipment = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", EQUIPMENT_NAME),
    ])
    if not equipment:
        return [f"Equipment {EQUIPMENT_NAME!r} not found"]
    if len(equipment) > 1:
        failures.append(
            f"Expected exactly 1 equipment named {EQUIPMENT_NAME!r}, found {len(equipment)}"
        )
    equipment = equipment[0]

    if not equipment.active:
        failures.append("Equipment is archived; expected it to remain active")

    if not equipment.category_id or equipment.category_id.name != CATEGORY_NAME:
        failures.append(
            f"Category is {equipment.category_id.name!r}, expected {CATEGORY_NAME!r}"
        )

    if (
        not equipment.technician_user_id
        or equipment.technician_user_id.name != TECHNICIAN_NAME
    ):
        failures.append(
            f"Technician is {equipment.technician_user_id.name!r}, "
            f"expected {TECHNICIAN_NAME!r}"
        )

    if equipment.expected_mtbf != EXPECTED_MTBF:
        failures.append(
            f"expected_mtbf is {equipment.expected_mtbf!r}, expected {EXPECTED_MTBF}"
        )

    if str(equipment.effective_date) != EFFECTIVE_DATE:
        failures.append(
            f"effective_date is {equipment.effective_date!s}, expected {EFFECTIVE_DATE}"
        )

    return failures
