# Cookbook notes — documents.upload_document_tag_assign_to_folder

## Feature availability audit: documents in Community

Odoo 19 Community does NOT ship the Documents app:

- `addons/documents/` does **not exist** on the `odoo_benchmark`
  branch.
- `grep -rn "documents.document" addons/` returns only 5 files, all
  of them soft references from orthogonal modules
  (`spreadsheet/static/tests/helpers/data.js`,
  `cloud_storage[_migration]/models/ir_attachment.py`,
  `account/{models,tests}/{ir_attachment,test_audit_trail}.py`) that
  gate on `env.get("documents.document")` — exactly the pattern used
  for optional-Enterprise-module integration. None of them register
  the model.
- No `documents.folder`, `documents.tag`, or `documents.facet`
  models.
- No `/odoo/documents` client action, no `documents_kanban` view,
  no `documents_inspector` Owl component.

The actual Documents workflow — the Workspaces tree, the Kanban of
document cards with previews, the **Upload** header button, the
drag-and-drop intake, the right-hand inspector panel (Folder / Tags /
Owner / Activities / Versions / Share link), the workflow rules
engine — is **Enterprise-only** (`documents` addon + optional
`documents_*_bridge` bridge modules for HR / Project / Account).

### Implications for task authors

- Any task that requires the agent to open Documents, click Upload,
  tag a file, set an owner, or configure a workflow rule is **not
  buildable** on Community.
- A workflow-adjacent task ("upload an attachment to a res.partner
  chatter") IS possible in Community — file it under `mail.*` /
  `base.*` without the `documents.` prefix.
- Before picking any `documents.*` task (upload, share, request,
  workflow rule, bridge record linking, split-PDF, etc.), confirm
  with:

  ```python
  module = env["ir.module.module"].search(
      [("name", "=", "documents")], limit=1)
  bool(module) and module.state == "installed"
  ```

  If False, the task is blocked until the enterprise addon is
  vendored.

## Pattern for BLOCKED-task commits (reminder)

Following the precedent set by
`appointment.public_booking_reschedule_cancel_portal`,
`helpdesk.team_sla_assign_escalate_close`,
`marketing_automation.tag_trigger_drip_campaign`,
`hr_skills_survey.link_certification_survey_to_skill`,
`stock_barcode.receive_via_barcode_scan_validate`, and
`account_followup.send_reminder_level_two_customers`, BLOCKED tasks
ship:

1. `task.yaml` with `metadata.blocked_reason` + `primary_track: false`
   + `version: "0.0-blocked"`.
2. `seed.py` / `oracle.py` / `check.py` that short-circuit with
   clear diagnostic `RuntimeError` / list-of-failures messages rather
   than silently passing. Each file should also carry a *commented*
   sketch of the real body so a future agent has a starting point
   once the constraint is lifted.
3. `expected_state.json = []` and `state_spec.yaml: models: {}` and
   empty `trace_spec` lists.
4. A `RESULT.md` recording the blocker evidence + re-enabling steps.
5. STATUS.md row set to `Removed` with `FAIL (module unavailable)`
   in the oracle column, plus a detailed section at the end.

## Precedent

- `stock_barcode.receive_via_barcode_scan_validate` (row 401) — same
  Enterprise-only addon pattern.
- `appointment.public_booking_reschedule_cancel_portal` (row 350)
- `helpdesk.team_sla_assign_escalate_close` (row 351)
- `marketing_automation.tag_trigger_drip_campaign` (row 352)
- `hr_skills_survey.link_certification_survey_to_skill` (row 387)
- `account_followup.send_reminder_level_two_customers` (row 404)
- `barcodes.receive_product_via_scan_validate`

All seven (including this task) share the same core shape:
Enterprise-only feature / addon absent in Community, skeleton
preserved for forward compatibility.
