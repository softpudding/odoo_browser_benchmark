# hr.generate_employee_card_set_badge_id — Result

- **Oracle:** PASS (F1 = 1.0, 1/1 atomic edits matched, wall_clock 29.3s)
- **Browser-Use (1 run):** PASS (F1 = 1.0, 1/1 atomic edits matched, wall_clock 86.4s, 23 non-forbidden writes, 0 forbidden)
- **Tier:** 2 (medium)
- **Difficulty verdict:** Small medium. Straightforward single-field edit on the HR Settings tab — BU solves it single-shot. Kept `primary_track=true` for its deterministic coverage of the `hr.employee.barcode` (a.k.a. "Badge ID") field + tab-switching navigation.

## Pre-flight deviation

- The user request asked for `badge_id`. In Odoo 19 there is **no** `badge_id` field on `hr.employee`; the employee-identification field is `barcode` (view label "Badge ID"). Pivoted to `barcode` per the pre-flight guidance. Constraint `_verify_barcode` enforces `[A-Za-z0-9]{1,18}` — chose `EMPBENCH001` (11 chars, all alphanumeric, no hyphens) to match the cookbook rule from `hr_attendance` quirks.

## Calibration notes

- Single field edit + tab switch. BU's 86s walltime is mostly initial login + app navigation — the actual field edit is a couple of seconds.
- Seeded employee has `barcode=False` so the state diff captures a clean `False -> 'EMPBENCH001'` transition and the "Print Badge" button (`invisible="not barcode"`) is hidden until after the agent saves.
- To harden to a real BU-failing task would need: (a) a wizard for badge generation (none ships in community), (b) a second employee as a distractor requiring disambiguation, or (c) forcing the agent to read a specific prefix rule from the prompt and generate a conforming value — but that pushes into hard tier.
