# maintenance.create_equipment_schedule_preventive_plan — Result

## Oracle
- **Status:** PASS
- **StateDiffF1:** 1.0
- **Wall clock:** 23.2 s
- 5 / 5 expected edits matched.

## Browser-Use (single-shot)
- **Status:** FAIL (Strict: FAIL)
- **StateDiffF1:** 0.0 (Precision 0.0, Recall 0.0)
- **Wall clock:** 290.4 s
- **Failure pattern:** Agent created **two** `Bench Press 01` equipment records (and two `Machinery` categories). The first record was saved complete with all fields including `effective_date=2026-06-01`; the agent then treated the "reopen and set Effective Date" step as "create a new equipment record" — the second record has `effective_date=2026-04-19` (today, from default).
- `check.py` caught it via `Expected exactly 1 equipment named 'Bench Press 01', found 2`.
- `state_diff` showed 10 atomic edits (5 matching first record, 5 extra on duplicate), producing F1=0.

## Design calibration
- **Core trap:** `expected_mtbf` is writable; `mtbf` is computed/readonly (ODOO19_PATTERNS). Prompt explicitly warns.
- **Secondary trap:** Two-phase save (save then reopen) encourages BU to duplicate-create on the second phase.
- **Category create-if-absent:** Seed deletes stale `Machinery` category so the agent must use the autocomplete "Create" shortcut.
