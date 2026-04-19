# Cookbook notes — account_followup.send_reminder_level_two_customers

## Feature availability audit: account_followup in Community

Odoo 19 Community does NOT ship any follow-up-reminder functionality:

- `addons/account_followup/` does **not exist** on the
  `odoo_benchmark` branch.
- `grep -rn "account_followup" addons/` returns **zero** matches (no
  model, no view, no controller, no i18n stub — nothing).
- The only follow-up-adjacent artefact is
  `addons/account/views/res_config_settings_views.xml:115`:

  ```xml
  <setting id="send_invoices_followups"
           help="Send invoices and payment follow-ups by post"
           documentation="/applications/finance/accounting/receivables/customer_invoices/snailmail.html">
      <field name="module_snailmail_account"/>
  </setting>
  ```

  This references `snailmail_account` (physical-mail invoicing), which
  is a different module that can optionally attach snail-mail copies
  to follow-up letters — but does NOT itself provide the follow-up
  reminder workflow.

The actual payment-reminder workflow — the `/odoo/action-account_followup.*`
routes, the Follow-up Reports list, the per-customer follow-up card
with Send Email / Send Letter / Schedule Activity header buttons, the
configurable `account_followup.followup.line` levels with per-level
email templates and delay days, the `followup_status` partner flag,
and the `account_followup_manual_reminder` wizard — is **Enterprise-only**
(`account_followup` addon + optional `account_followup_batch_sending`
sibling).

### Implications for task authors

- Any task that requires the agent to open Follow-up Reports, use the
  per-customer follow-up card, click Send Email on a follow-up, or
  configure follow-up levels is **not buildable** on Community.
- A workflow-adjacent task ("send a chatter email from an overdue
  invoice") IS possible in Community — file it under `account.*` or
  `mail.*` without the `account_followup.` prefix.
- Before picking any `account_followup.*` task (manual reminder,
  batch reminders cron, level escalation, letter via snailmail,
  activity scheduling from follow-up card, etc.), confirm with:

  ```python
  module = env["ir.module.module"].search(
      [("name", "=", "account_followup")], limit=1)
  bool(module) and module.state == "installed"
  ```

  If False, the task is blocked until the enterprise addon is vendored.

## Pattern for BLOCKED-task commits (reminder)

Following the precedent set by `appointment.public_booking_reschedule_cancel_portal`,
`helpdesk.team_sla_assign_escalate_close`,
`marketing_automation.tag_trigger_drip_campaign`,
`hr_skills_survey.link_certification_survey_to_skill`,
`stock_barcode.receive_via_barcode_scan_validate`, and the earlier
`barcodes.receive_product_via_scan_validate`, BLOCKED tasks ship:

1. `task.yaml` with `metadata.blocked_reason` + `primary_track: false`
   + `version: "0.0-blocked"`.
2. `seed.py` / `oracle.py` / `check.py` that short-circuit with clear
   diagnostic `RuntimeError` / list-of-failures messages rather than
   silently passing. Each file should also carry a *commented* sketch
   of the real body so a future agent has a starting point once the
   constraint is lifted.
3. `expected_state.json = []` and `state_spec.yaml: models: {}` and
   empty `trace_spec` lists.
4. A `RESULT.md` recording the blocker evidence + re-enabling steps.
5. STATUS.md row set to `Removed` with `FAIL (module unavailable)` in
   the oracle column, plus a detailed section at the end.

## Precedent

- `stock_barcode.receive_via_barcode_scan_validate` (row 401) — same
  Enterprise-only addon pattern.
- `appointment.public_booking_reschedule_cancel_portal` (row 350)
- `helpdesk.team_sla_assign_escalate_close` (row 351)
- `marketing_automation.tag_trigger_drip_campaign` (row 352)
- `hr_skills_survey.link_certification_survey_to_skill` (row 387)
- `barcodes.receive_product_via_scan_validate`

All six (including this task) share the same core shape:
Enterprise-only feature / addon absent in Community, skeleton preserved
for forward compatibility.
