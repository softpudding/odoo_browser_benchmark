ROW: 370
TASK_ID: project_todo.bulk_move_tasks_between_projects
DIFFICULTY: hard
SUMMARY: Reassign 3 of 4 tasks (Alpha/Bravo/Charlie — but NOT distractor Delta) from 'Bench Proj A' to empty 'Bench Proj B' by editing each task's Project field on the form view.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: pivoted_from_bulk_wizard_to_per_task_form_edit

DETAIL_SECTION:
## project_todo.bulk_move_tasks_between_projects

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Seed creates two projects `Bench Proj A` (4 tasks: Alpha/Bravo/Charlie/Delta) and `Bench Proj B` (empty). Agent opens each of Alpha/Bravo/Charlie in the task form, changes the `Project` many2one from Proj A to Proj B, and Saves — three times. Delta must remain in Proj A as a distractor. Final: Proj A has 1 task (Delta), Proj B has 3 (Alpha/Bravo/Charlie). |
| **Capability tested** | Repeated form-edit of a many2one field across 3 similar records without touching the 4th distractor. Originally scoped as "multi-select + bulk 'Move to Project' action" but **no such action exists in Odoo 19 Community** — `project.task` has no move-to-project wizard, and the `project_id` column in `project_task_view_tree_main_base` is declared `readonly="1"`, so list inline edit is blocked too. Canonical path is per-task form edit. |
| **Notes** | Calibration pivot: bulk wizard / list inline-edit pattern was unavailable (see ODOO19_PATTERNS entry); fell back to per-task form edit of project_id × 3. Oracle uses JSON-RPC `web_save` for determinism. Browser-use moved only **Alpha** (1/3) then hallucinated an access-rights error and gave up despite the admin user clearly having write permission — classic BU misfire on repeated form-hop workflows. Genuine hard-tier FAIL: state_diff F1=0.0 (engine treats partial-matches as 0), 4 postcondition failures. BU wall-clock 161 s before abort, well inside the 480 s budget. |
