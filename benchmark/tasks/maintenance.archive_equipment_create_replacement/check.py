"""Postcondition checks for maintenance.archive_equipment_create_replacement."""


def check(env):
    failures = []

    # --- Old equipment must be archived (active=False) ---
    old = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "Old Belt OB-99"),
    ])
    if not old:
        failures.append("Equipment 'Old Belt OB-99' not found (was it deleted?)")
    elif len(old) > 1:
        failures.append(
            f"Expected exactly 1 equipment named 'Old Belt OB-99', found {len(old)}"
        )
    else:
        old = old[0]
        if old.active:
            failures.append(
                "Equipment 'Old Belt OB-99' is still active; expected it to be archived"
            )

    # --- New equipment must exist, active, with the right category and serial ---
    new = env["maintenance.equipment"].with_context(active_test=False).search([
        ("name", "=", "New Belt NB-100"),
    ])
    if not new:
        return failures + ["Equipment 'New Belt NB-100' not found"]
    if len(new) > 1:
        failures.append(
            f"Expected exactly 1 equipment named 'New Belt NB-100', found {len(new)}"
        )
    new = new[0]

    if not new.active:
        failures.append(
            "Equipment 'New Belt NB-100' is archived; expected it to remain active"
        )

    if new.serial_no != "NB-100-SN-2026":
        failures.append(
            f"New equipment serial number is {new.serial_no!r}, expected 'NB-100-SN-2026'"
        )

    if not new.category_id or new.category_id.name != "Warehouse Gear":
        failures.append(
            f"New equipment category is {new.category_id.name!r}, expected 'Warehouse Gear'"
        )

    return failures
