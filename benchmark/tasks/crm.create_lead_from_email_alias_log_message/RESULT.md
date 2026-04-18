ROW: 325
TASK_ID: crm.create_lead_from_email_alias_log_message
DIFFICULTY: hard
SUMMARY: Configure CRM team 'Inbound' with alias leads-inbound + Accept Emails From 'Authenticated Partners', create a lead 'Inbound Inquiry from Sample' with email prospect@external.test, priority Medium (1 star) and tag 'Website', then post a chatter message.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## crm.create_lead_from_email_alias_log_message

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | CRM (+ mail.alias, crm.team) |
| **Workflow** | Configure a CRM team's Email Alias (mid-form inline input) and change Accept Emails From from 'Everyone' to 'Authenticated Partners' (o_select_menu dropdown, NOT native select); create a new `crm.lead` via Leads menu with name, email_from, priority=Medium (single star), and an existing `Website` tag; post a regular chatter message 'Asked about Bench Pro pricing.' (not a log note). Three distinct navigation surfaces plus multiple calibration traps. |
| **Capability tested** | Three-surface workflow (team config + lead create + chatter message) combining a non-default Odoo select-menu dropdown, single-star priority pitfall, many2many tag autocomplete, and the Send-message-vs-Log-note distinction. |
| **Notes** | First pass (before hardening): BU trivially passed F1=1.0/postcond-clean because the alias edit and chatter are both visually obvious and the first BU trial auto-set alias. Hardened by adding (a) alias_contact -> Authenticated Partners (custom `o_select_menu`, not a native `<select>`), (b) priority=Medium (single star, canonical BU trap), (c) mandatory `Website` tag on the lead. Post-hardening BU nailed state diff 5/5 but skipped the tag -> postcondition FAIL. Oracle uses `.o_select_menu_toggler` click + `.o_select_menu_item:has-text(...)` pattern for `alias_contact`. `crm.lead.name` is rendered with widget="text" (textarea) so `fill_field` on `input` times out; must use `fill_text_field`. |
