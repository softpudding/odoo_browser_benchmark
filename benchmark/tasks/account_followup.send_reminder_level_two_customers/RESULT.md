# account_followup.send_reminder_level_two_customers — RESULT

## Verdict: REMOVED (module unavailable — Enterprise-only)

This task is blocked because the `account_followup` addon is an **Odoo
Enterprise** module that is not vendored in this Odoo 19 Community
codebase. The Follow-up Reports / Customer Statement backend screen
(list of customers-with-overdue-balances, per-customer follow-up card
with **Send Email** / **Send Letter** / **Schedule Activity** header
buttons, default reminder template per level, `mail.mail` auto-send
with invoice PDFs attached) ships entirely inside `account_followup`.

## Evidence

Inspected `addons/` on branch `odoo_benchmark`:

```
$ ls addons/ | grep -iE "followup|account_fol"
(no matches)

$ grep -rn "account_followup" addons/
(no matches)

$ grep -rn "followup|follow_up|follow-up" addons/account/ -i | head
addons/account/views/res_config_settings_views.xml:115:
    <setting id="send_invoices_followups"
             help="Send invoices and payment follow-ups by post">
        <field name="module_snailmail_account"/>
    </setting>
# (the setting points at snailmail_account, NOT a follow-up workflow)
```

Key findings:

- There is NO `addons/account_followup/` directory.
- `grep -rn "account_followup" addons/` returns **zero** matches: no
  model, no view, no controller, no client action, no security rule,
  no i18n string (which means the Enterprise module was never even
  shipped as a stub in this checkout).
- The only follow-up-related artefact is the `send_invoices_followups`
  upgrade_boolean in Accounting Settings which targets the orthogonal
  `snailmail_account` module (physical-mail invoicing, NOT the
  per-partner reminder workflow).
- No `account_followup.followup.line` (configurable levels), no
  `account_followup.followup.report` client action, no
  `account_followup_manual_reminder` wizard, no
  `res.partner.followup_status` / `followup_line_id` /
  `followup_next_action_date` fields exist in this codebase.
- Attempting to install via
  `env["ir.module.module"].search([("name","=","account_followup")]).button_immediate_install()`
  would fail with "Module not found" because the addon source isn't
  present on disk.

The task's central step ("open the follow-up card, click **Send
Email**") therefore cannot be executed — there is no such screen in
Community. Seeding 3 overdue `account.move` rows for
`Bench Overdue Co` would succeed technically, but the agent would
land on a 404 when navigating to `/odoo/action-account_followup.*`.

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
- `barcodes.receive_product_via_scan_validate` — same `stock_barcode`
  absence, earlier attempt.

All use the same BLOCKED-skeleton pattern: short-circuit seed / oracle /
check with diagnostic errors, ship empty `expected_state.json` +
`state_spec: {}` + `trace_spec: []`, STATUS row set to Removed with
`FAIL (module unavailable)`.

## Lifecycle status

- Pre-flight: FAILED — `ls addons/account_followup/` returned
  "No such file or directory"; `grep -rn "account_followup" addons/`
  returned zero matches.
- Oracle: did NOT run (short-circuits with RuntimeError).
- BU: did NOT run.
- F1: N/A.
- Calibration: N/A.

## Re-enabling

To re-enable, vendor the enterprise `account_followup` addon into
`addons/`. Then:

1. Replace the `raise RuntimeError` / `raise NotImplementedError`
   guards in `seed.py` with the real seed (sketch is already in the
   comment block at the bottom of `seed.py`).
2. Flesh out `oracle.py` with the three-phase flow documented in the
   module docstring. Verify selector names against the current
   enterprise Follow-up Report client (`.o_followup_report`,
   `.o_followup_line_header_name`, `button[name='action_send_mail']`,
   or their current equivalents).
3. Flesh out `check.py` to assert (a) partner `Bench Overdue Co`
   exists, (b) 3 posted `account.move` rows exist with the expected
   names / due date / amounts, (c) at least one `mail.message` logged
   on the partner whose body references all three invoice names, and
   (d) the partner's `followup_status` flag advanced.
4. Populate `state_spec.yaml` + `expected_state.json` from a real
   run's `state_diff.json` (will contain `res.partner`,
   `account.move`, `mail.message`, `mail.mail` entries).
5. Flip STATUS row 404 from Removed → WIP and re-run the normal
   lifecycle.
