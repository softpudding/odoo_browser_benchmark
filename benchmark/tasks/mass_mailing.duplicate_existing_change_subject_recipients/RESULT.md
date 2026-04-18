ROW: 310
TASK_ID: mass_mailing.duplicate_existing_change_subject_recipients
DIFFICULTY: medium
SUMMARY: Duplicate seeded draft mailing via Actions menu; on copy change subject + recipients model + Country=Germany filter.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## mass_mailing.duplicate_existing_change_subject_recipients

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Email Marketing |
| **Workflow** | Open seeded draft mailing 'Q1 Bulletin Template' in Email Marketing. Use the cog/Actions menu Duplicate to make a copy. On the copy, change Subject to 'Q2 Bulletin Update', switch the Recipients dropdown from Mailing List to Contact, and add a single domain rule Country = Germany; save as draft (do not send). |
| **Capability tested** | Multi-field edit on a duplicated record (Action menu Duplicate) without modifying the original; combines hidden cog menu, recipients-model swap, and domain editor with country lookup. |
| **Notes** | BU spammed the cog->Duplicate path repeatedly, leaving 14 extra unmodified copies (hit step limit). Oracle uses JSON-RPC (mailing.copy + write) because the domain widget + Recipients autocompletion are too brittle for Playwright (same rationale as sibling mass_mailing.create_segmented_mailing_save_draft oracle). check.py validates: original untouched (mailing_model_name='mailing.list', draft, no sent_date), duplicate has res.partner + Country=Germany domain (resolves country_id by id/name/'DE' code), exactly 2 mailings exist. |
