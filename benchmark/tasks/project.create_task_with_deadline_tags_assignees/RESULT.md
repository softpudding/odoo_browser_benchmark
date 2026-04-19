ROW: 409
TASK_ID: project.create_task_with_deadline_tags_assignees
DIFFICULTY: medium
SUMMARY: In 'Bench Tag Proj', create a new project.task 'Fix login bug' with date_deadline 06/30/2026, two tag_ids (urgent, backend), and two user_ids assignees (Mitchell Admin + Bench Dev 2).
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: miss  (BU passed single-shot)

DETAIL_SECTION:
## project.create_task_with_deadline_tags_assignees

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 33.4s) |
| **Browser-Use** | PASS (F1=1.0, 94.0s, 12 steps) |
| **F1** | 1.0 |
| **Odoo modules** | Project |
| **Workflow** | Seed creates empty project 'Bench Tag Proj', pre-existing project.tags 'urgent' + 'backend', and a second internal user 'Bench Dev 2' with project.group_project_user. Agent opens the project kanban, clicks New, fills Title=`Fix login bug`, Deadline=`06/30/2026` (Tab to close datepicker), picks the two existing tags via tag_ids autocomplete, picks both assignees on user_ids, saves. |
| **Capability tested** | Multi-field task form creation: datetime Deadline + many2many_tags existing-pick + many2many user assignees with a non-default second user. |
| **Notes** | Calibration miss — BU handles the four-field form cleanly. date_deadline is fields.Datetime (project_task.py:183), so UTC->admin-local TZ conversion needed in check.py. expected_state.json requires both `name` and `active=True` create edits (fresh records emit both). trace_spec forbids project.tags.create / res.users.create so a quick-create substitution would fail HarmfulWriteRate. |
