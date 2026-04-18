# Register a New Preventive-Plan Equipment

Open the **Maintenance** app and create a new equipment record with a simple preventive-maintenance plan.

## Steps

1. Open **Maintenance → Equipments**.
2. Click **New**.
3. Set the **Name** to `Bench Press 01`.
4. Set the **Equipment Category** to `Machinery`. This category does **not** exist yet — create it from the category dropdown (e.g. via "Create" in the autocomplete).
5. Set the **Technician** to `Bench Tech` (the user already exists; pick it from the autocomplete).
6. Open the **Maintenance** tab and set **Expected Mean Time Between Failure** to `30` days. (This is the writable `Expected MTBF` field — do NOT try to edit `MTBF`, which is a read-only computed statistic.)
7. **Save** the equipment.
8. Reopen the saved equipment, go to the **Product Information** tab, and set the **Effective Date** to `06/01/2026`.
9. **Save** the record.

## Rules

- Use the exact name, category, technician, Expected MTBF, and Effective Date shown above.
- The `Machinery` category does not exist yet — create it on the fly.
- The `Bench Tech` user already exists — select them, do not create a new user.
- Leave the new equipment active (do not archive it).
- Do not modify or delete any other equipment, category, or user record.
