# Cookbook notes — hr.add_skill_to_employee_with_level

## New / reinforced quirks

- `hr_skills` is NOT listed in `benchmark/base_modules.txt`, but the base snapshot still has it installed — `hr_recruitment_skills` is `auto_install=True` with deps `[hr_skills, hr_recruitment]`, and hr_recruitment is in the base. So the module exists without an explicit entry. A defensive `button_immediate_install` in the seed is still harmless and recommended for portability.
- Employee form: the "Skills" section is inside the **Resume** tab (lower half of the tab), not a top-level "Skills" tab. `click_tab(page, "Resume")` is the correct call.
- `Pick a skill from the list` opens a modal with Odoo's `o_selection_badge` widget — three cascading badge groups: `skill_type_id` → `skill_id` → `skill_level_id`. The Skill and Level badge sets refresh after the Skill Type is chosen.
- For the skill picker, prefer `.o_selection_badge:has-text('<name>')` scoped under `[name='<field>']` to avoid mis-clicking label chrome.
- Diff engine normalizes `employee_id` and `skill_id` (Many2one) to their display names — use those as the entity_key pair to get stable keys across runs.

## Differentiation from hr.add_employee_skill

- Employee: `Tech Tom` (vs Priya Mehta).
- Skill Type: `Programming Languages` (vs IT Skills).
- Same Skill=Python, Level=Advanced — but the skill_type_id foreign key differs, so `hr.employee.skill` match_key `[employee_id, skill_id]` yields a disjoint entity_key.

## Browser-use behavior

- BU navigated Resume tab, opened the "Pick a skill" modal, and used the badge selection correctly. Wall clock ~82s. No retries or recovery needed. Task passes BU on single-shot.
