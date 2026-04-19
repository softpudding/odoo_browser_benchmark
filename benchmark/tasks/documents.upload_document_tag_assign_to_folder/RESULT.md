# documents.upload_document_tag_assign_to_folder — RESULT

## Verdict: REMOVED (module unavailable — Enterprise-only)

This task is blocked because the `documents` addon is an **Odoo
Enterprise** module that is not vendored in this Odoo 19 Community
codebase. The Documents app (Workspaces Kanban, Upload header
button, per-document inspector side panel with Folder / Tags / Owner
fields, drag-and-drop file intake) ships entirely inside the
`documents` addon.

## Evidence

Inspected `addons/` on branch `odoo_benchmark`:

```
$ ls addons/documents/
ls: addons/documents/: No such file or directory

$ ls addons/ | grep -i "document\|dms"
l10n_latam_invoice_document
# (unrelated LATAM invoice document type module)

$ grep -rn "documents.document" addons/
addons/spreadsheet/static/tests/helpers/data.js
addons/cloud_storage_migration/models/ir_attachment.py
addons/cloud_storage/models/ir_attachment.py
addons/account/tests/test_audit_trail.py
addons/account/models/ir_attachment.py
# (5 files — all soft references that gate on env.get("documents.document")
#  or mock it in spreadsheet test helpers; none register the real model.)
```

Key findings:

- There is NO `addons/documents/` directory.
- `grep -rn "documents.document" addons/` returns only 5 soft
  references, none of which implement the model. The references are:
  - `spreadsheet/static/tests/helpers/data.js` — a mock factory for
    JS unit tests that does not require the real model at runtime.
  - `cloud_storage/models/ir_attachment.py` and
    `cloud_storage_migration/models/ir_attachment.py` — both guard
    their handling with `env.get("documents.document")`, a pattern
    used precisely for optional-enterprise-module integration.
  - `account/tests/test_audit_trail.py` and
    `account/models/ir_attachment.py` — same guarded optional
    integration.
- No `documents.folder` / `documents.tag` / `documents.facet` models
  exist in Community.
- No `/odoo/documents` client action; no `documents_kanban` view;
  no `documents_inspector` Owl component.
- Attempting to install via
  `env["ir.module.module"].search([("name","=","documents")]).button_immediate_install()`
  would fail with "Module not found" because the addon source isn't
  present on disk.

The task's central step ("click Upload in the Documents header and
pick a file") therefore cannot be executed — there is no Documents
screen in Community.

## Precedent

Tasks Removed on the same grounds (Enterprise-only addon / feature
missing in Community):

- `stock_barcode.receive_via_barcode_scan_validate` (row 401) —
  `stock_barcode` Enterprise-only.
- `appointment.public_booking_reschedule_cancel_portal` (row 350) —
  `appointment` addon uninstallable.
- `helpdesk.team_sla_assign_escalate_close` (row 351) — `helpdesk`
  module absent.
- `marketing_automation.tag_trigger_drip_campaign` (row 352) —
  `marketing_automation` absent.
- `hr_skills_survey.link_certification_survey_to_skill` (row 387) —
  `hr.skill.survey_id` Enterprise-only.
- `account_followup.send_reminder_level_two_customers` (row 404) —
  `account_followup` Enterprise-only.

All use the same BLOCKED-skeleton pattern: short-circuit seed / oracle /
check with diagnostic errors, ship empty `expected_state.json` +
`state_spec: {}` + `trace_spec: []`, STATUS row set to Removed with
`FAIL (module unavailable)`.

## Lifecycle status

- Pre-flight: FAILED — `ls addons/documents/` returned
  "No such file or directory"; `grep -rn "documents.document" addons/`
  returned 5 files of soft-reference-only matches.
- Oracle: did NOT run (short-circuits with RuntimeError).
- BU: did NOT run.
- F1: N/A.
- Calibration: N/A.

## Re-enabling

To re-enable, vendor the enterprise `documents` addon into
`addons/`. Then:

1. Replace the `raise RuntimeError` / `raise NotImplementedError`
   guards in `seed.py` with the real seed (sketch is already in the
   comment block at the bottom of `seed.py`). Key records to seed:
   - `documents.folder` named `Bench Folder`.
   - `documents.facet` + `documents.tag` hierarchy for the `invoice`
     tag scoped to that folder.
   - A deterministic `/tmp/bench_documents_sample.pdf` file on disk
     (minimal valid PDF) so the browser file-picker has something
     concrete to upload.
2. Flesh out `oracle.py` with the four-phase flow documented in the
   module docstring. Verify selector names against the current
   enterprise Documents client (`.o_documents_view`,
   `.o_documents_inspector`, `.o_search_panel`, or their current
   equivalents). Playwright `page.expect_file_chooser()` must be
   wrapped around the Upload click.
3. Flesh out `check.py` to assert (a) exactly one
   `documents.document` in `Bench Folder` with `tag_ids` containing
   `invoice`, `owner_id == admin`, and a non-empty
   `attachment_id.name`; (b) the folder + tag are unmodified; (c) no
   other documents were created.
4. Populate `state_spec.yaml` + `expected_state.json` from a real
   run's `state_diff.json` (will contain `documents.document`,
   `ir.attachment`, and possibly `mail.message` entries for the
   create audit note).
5. Flip STATUS row 411 from Removed → WIP and re-run the normal
   lifecycle.
