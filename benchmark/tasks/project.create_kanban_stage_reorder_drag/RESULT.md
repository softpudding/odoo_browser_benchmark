ROW: 326
TASK_ID: project.create_kanban_stage_reorder_drag
DIFFICULTY: medium
SUMMARY: In Bench Project A kanban, create stage 'Backlog Review' via Add column quick-create, then drag-reorder to position #2 (between Triage and In Progress).
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## project.create_kanban_stage_reorder_drag

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Project |
| **Workflow** | Open seeded project 'Bench Project A' (grouped kanban of its tasks with pre-seeded stages Triage/In Progress/Review/Done). Unfold the `.o_column_quick_create` chevron at the right edge, type 'Backlog Review', confirm. Then drag the new 'Backlog Review' column header leftward so it drops between 'Triage' and 'In Progress'. |
| **Capability tested** | Kanban column quick-create + column drag-reorder (web_resequence via Owl's useSortable) — a UI interaction pattern distinct from the existing card-drag task (project.kanban_drag_task_between_stages), since it moves GROUPS not RECORDS and involves two web_resequence RPCs (one implicit on create, one on drag). |
| **Notes** | Oracle uses an emulated slow mouse drag on the `.o_column_title` handle (the `KanbanRenderer` useSortable config pins `handle: ".o_column_title"`). Browser-use created 'Backlog Review' correctly (single `name_create` + auto `web_resequence` to place at end) but could NOT drag the column to position #2 — left it at position #5 (far right). Classic drag-reorder failure mode predicted in the backlog calibration note. Seed intentionally uses sparse sequences (10/20/30/40) so the kanban's reorderAll branch renumbers everything starting at min(sequences)=1 on the first web_resequence; check.py is sequence-agnostic and validates left-to-right ordering instead. |
