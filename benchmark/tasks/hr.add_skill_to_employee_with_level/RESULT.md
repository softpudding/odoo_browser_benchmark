# hr.add_skill_to_employee_with_level — Result

- **Oracle:** PASS (F1 = 1.0, 4/4 atomic edits matched, wall_clock 31.4s)
- **Browser-Use (1 run):** PASS (F1 = 1.0, 4/4 atomic edits matched, wall_clock 82.0s)
- **Tier:** 2 (medium)
- **Difficulty verdict:** Medium — browser-use solves the cascading-dropdown skill picker cleanly. Not a reliable hard-tier fail; primary_track=true retained since the check is deterministic and the task exercises the cascading o_selection_badge UI.

## Calibration notes

- Seed installs `hr_skills` on demand (`button_immediate_install`) to match the ODOO19_PATTERNS guidance, though it happens to already be pulled in via the base snapshot (transitively through hr_recruitment_skills auto-install).
- Skill type **Programming Languages** is seeded fresh (distinct from the **IT Skills** type used by `hr.add_employee_skill`) so entity keys `[employee_id, skill_id]` do not collide with the sibling task.
- No pre-existing `hr.employee.skill` row for Tech Tom; the agent must create it.
- 4 expected diff rows: `employee_id`, `skill_id`, `skill_type_id`, `skill_level_id` on the new `hr.employee.skill`.
