ROW: 301
TASK_ID: website_slides.duplicate_lesson_to_new_section
DIFFICULTY: medium
SUMMARY: Add Advanced section, duplicate Welcome Video lesson via Actions menu, move duplicate to Advanced and rename to Advanced Welcome.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## website_slides.duplicate_lesson_to_new_section

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (eLearning) |
| **Workflow** | Open Bench Onboarding Course (seeded with Intro section + Welcome Video lesson). Add new section Advanced, then duplicate Welcome Video via the cog/Actions menu, move the copy into Advanced via the section Many2one, and rename it to Advanced Welcome. |
| **Capability tested** | Sub-resource duplication via cog/Actions Duplicate menu plus section reassignment of a slide.slide whose section is sequence-derived, not a directly editable Many2one. |
| **Notes** | Browser-use duplicated the entire course three times instead of duplicating the lesson, exposing the cog-menu navigation hazard the task targets. Oracle uses copy() + sequence rewrite because slide.slide.category_id is computed from sequence ordering. |
