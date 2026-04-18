ROW: 303
TASK_ID: maintenance.archive_equipment_create_replacement
DIFFICULTY: medium
SUMMARY: Archive seeded equipment 'Old Belt OB-99' via Actions, then create replacement 'New Belt NB-100' with serial in same category.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## maintenance.archive_equipment_create_replacement

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1 1.0, 97.4s) |
| **F1** | 1.0 |
| **Odoo modules** | Maintenance |
| **Workflow** | Open the seeded equipment 'Old Belt OB-99' in category Warehouse Gear and archive it via the form Actions menu. Then create a new equipment 'New Belt NB-100' in the same Warehouse Gear category with serial 'NB-100-SN-2026', and save. |
| **Capability tested** | Two-step lifecycle on the same model: archive existing record (active=False) via Actions menu, then create-from-scratch a replacement with exact category and serial. |
| **Notes** | Archive sets `active=False` which the diff engine normalizes to `null` (matches the unchecked-Boolean note in ODOO19_PATTERNS.md). The create-from-scratch on `maintenance.equipment` also generates an explicit `active=true` create entry — both must be encoded in expected_state.json. Browser-use solved it on first attempt; calibration trends easier than medium. |
