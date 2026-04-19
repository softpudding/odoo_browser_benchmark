ROW: 403
TASK_ID: hr_recruitment.create_applicant_kanban_move_to_offer
DIFFICULTY: medium
SUMMARY: Seed a job "Bench Senior Dev" with stages Initial Qualification / Qualified / Contract Proposal / Contract Signed. Agent opens the job's Applications kanban, uses the Initial Qualification column's + New quick-create to add an applicant (partner_name 'Alice Applicant'), opens the full form to fill email 'alice@bench.test' and phone '+15555555555', saves, then advances the status bar twice to land in Contract Proposal.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## hr_recruitment.create_applicant_kanban_move_to_offer

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Recruitment (hr_recruitment) |
| **Workflow** | Seed creates an `hr.job` named `Bench Senior Dev` (department `Bench Engineering`) plus four job-scoped `hr.recruitment.stage` records (`Initial Qualification`, `Qualified`, `Contract Proposal`, `Contract Signed`, sequences 10/20/30/40). No applicants seeded. Agent opens `/odoo/recruitment`, clicks the Bench Senior Dev kanban card, lands on the Applications kanban grouped by stage, clicks the `+` on the Initial Qualification column, types `Alice Applicant`, confirms. Then clicks the new card to open the full form, fills `email_from=alice@bench.test` + `partner_phone=+15555555555`, saves, and advances the status bar through `Qualified` → `Contract Proposal`. |
| **Capability tested** | Kanban per-column quick-create (`button.o_kanban_quick_add` + quick-create partner_name input + green-check confirm), reopening the newly-created card to reach the full form, exact-value field entry on `hr.applicant.email_from` / `partner_phone`, and form status-bar stage advancement (widget `rotting_statusbar_duration` with `clickable=1`). Stages must be job-scoped via `hr.recruitment.stage.job_ids` so the Applications kanban has exactly four columns in the seeded order. |
| **Notes** | **Calibration: easier.** BU passed first-run in ~76s with F1=1.0; oracle took ~36s. The task is on the easy side of the medium band — quick-create + open-form + two status-bar clicks is linear with no wizard modal and no radio-disambiguation, and Claude-driven BU handles each of those individually. It still validates genuine kanban UI interaction (not a pure form edit), so tier=2 is appropriate. To harden to tier 3, add a non-default wizard (e.g. kanban-action `Send Email`) or force a kanban drag-drop between columns. Default hr_recruitment demo stages are `New` / `Qualification` / `First Interview` / `Second Interview` / `Contract Proposal` / `Contract Signed` — seed creates its own job-scoped stages with the prompt's exact names. |
