ROW: 402
TASK_ID: hr_holidays.request_allocation_approve_self_book_day_off
DIFFICULTY: hard
SUMMARY: From Time Off Management, create + approve a 5-day `Bench Bonus Days` allocation for Bench Worker, then create + approve a 1-day leave on 2026-05-15 against it. Two-phase cross-flow where the allocation must validate before the leave can validate.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier-than-expected

DETAIL_SECTION:
## hr_holidays.request_allocation_approve_self_book_day_off

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | HR Holidays (Time Off) |
| **Workflow** | Two-phase record creation on `/odoo/time-off-approval`: (1) Management -> Allocations -> New: employee=Bench Worker, type=Bench Bonus Days, 5 days, desc `Q2 bonus`, save -> Approve to `state='validate'`. (2) Management -> Time Off -> New: same employee + type, desc `Bench day off`, single-day 2026-05-15, save -> Approve to `state='validate'`. The `Bench Bonus Days` type has `requires_allocation='yes'` + `allocation_validation_type='hr'`, so the leave refuses to validate until the allocation does. |
| **Capability tested** | Sequential two-record cross-flow with a server-side ordering constraint. Each record requires its own Approve click after Save, so the agent must not forget the second state transition. BU handled both phases sequentially with 35 non-forbidden writes across 196s. |
| **Notes** | Spec called for `allocation_validation_type='officer'` but that value does not exist in Odoo 19 (valid choices: `no_validation` / `manager` / `both` / `hr`); used `'hr'` which preserves the Confirm -> Approve lifecycle. Task is calibrated easier than intended — browser-use cleanly passed (F1=1.0, required ops = both `.action_approve` hit, 0 forbidden writes). Consider escalating this workflow with a non-default wizard choice or a calibration trap (e.g., a distractor allocation that must stay untouched, or a leave type requiring a non-default `request_unit`) if stricter difficulty is needed. |
