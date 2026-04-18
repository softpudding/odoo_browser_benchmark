ROW: 311
TASK_ID: hr_holidays.refuse_then_re_request_other_type
DIFFICULTY: hard
SUMMARY: Manager refuses Eve's Paid Time Off, posts reason in chatter, then creates Sick Time Off on her behalf for same dates.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.7059
CALIBRATION: matches

DETAIL_SECTION:
## hr_holidays.refuse_then_re_request_other_type

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (gave_up at 480s; strict FAIL, F1 0.7059) |
| **F1** | 0.7059 |
| **Odoo modules** | Time Off |
| **Workflow** | Admin (leave manager) opens Eve Employee's pending Paid Time Off request, clicks Refuse, posts the refusal reason "Use sick leave instead" as a chatter message, then creates a NEW Sick Time Off request on Eve's behalf via the manager approval list, same dates (08/10/2026-08/12/2026), and saves it to land in 'confirm' (To Approve) state. |
| **Capability tested** | Two-step lifecycle on different records: refuse one leave + chatter message, then create-on-behalf-of-employee with a different leave type and exact dates. |
| **Notes** | hr.leave has no native `refuse_reason` field; the reason is captured as a chatter mail.message body (mirrors hr_holidays.refuse_leave_with_reason). Manager-only validation type lets the new Sick Time Off land in 'confirm' immediately on save. BU created a duplicate leave (one with 0 days) before producing the correct 3-day record, which produced extra state-diff edits and dropped strict F1 to 0.7059 — semantic check.py still passed (the correct record exists), but strict scoring penalises the dup. |
