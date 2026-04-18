ROW: 314
TASK_ID: crm.assign_team_change_salesperson_log_activity
DIFFICULTY: medium
SUMMARY: Reassign opportunity to Channel team + Sara Sales salesperson, then schedule a 2026-06-10 Discovery Call activity.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## crm.assign_team_change_salesperson_log_activity

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | CRM |
| **Workflow** | Open opportunity 'Bench Big Deal'; switch Salesperson Many2one from Mitchell Admin to Sara Sales (top of form); open the 'Contacts' notebook tab and switch Sales Team Many2one from Direct Sales to Channel under Ownership; save; schedule a Call activity dated 2026-06-10 with summary 'Discovery call' via the chatter Activities button. |
| **Capability tested** | Two distinct Many2one swaps in different form regions (chatter-area avatar widget vs notebook tab) plus a multi-field activity-scheduling modal. |
| **Notes** | Browser-use solved this on first try (F1=1.0) — proved easier than expected. Worth noting: in Odoo 19 the opportunity form hides team_id from the main "Sales" group (`invisible="type == 'opportunity'"`); the editable team_id field only appears in the Contacts > Ownership group. Prompt explicitly directs the agent to that tab. Sara Sales user and the Direct Sales / Channel teams are seeded by setup() since base data only ships the "Sales" team. |
