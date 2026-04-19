ROW: 451
TASK_ID: hr_holidays.request_sick_leave_approve_self
DIFFICULTY: hard
SUMMARY: From Time Off, create a Sick Leave request for Bench Sick Employee for 2026-05-11 -> 2026-05-12, then switch to the Management / Approvals dashboard and approve the request so it reaches state='validate'. Two-phase submit-then-approve lifecycle with datetime widget entry + cross-view context switch.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: as-intended

DETAIL_SECTION:
## hr_holidays.request_sick_leave_approve_self

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | HR Holidays (Time Off) |
| **Workflow** | Start on `/odoo/time-off`. Click New Request / New, fill Time Off Type=Sick Leave, Employee=Bench Sick Employee, dates 2026-05-11 -> 2026-05-12, description `Sick leave benchmark`. Save -> the request lands in `state='confirm'` (To Approve). Navigate to `/odoo/time-off-approval` (Management / Approvals), find the pending request, click Approve -> state flips to `validate`. |
| **Capability tested** | Two-step role lifecycle (employee submit + manager approve) across two distinct Odoo views, plus datetime widget entry for start/end of the sick leave. `Sick Leave` type is pre-configured by the seed with `requires_allocation=False` and `leave_validation_type='hr'` so admin (who has the HR + manager groups) can approve directly; there is no `action_confirm` in Odoo 19 — state defaults to `'confirm'` on create. Browser-use exhausted the 420s time limit stuck on the new-request form: never advanced past the default start/end date of today (2026-04-19), never reached the Approvals dashboard, so `action_approve` was never called; final state stayed `confirm` with `number_of_days=0.0`. F1=0.0, RequiredOpRecall=0.0. |
| **Notes** | Calibrated as intended — the date-picker + cross-view approval combination cleanly fails BU. In Odoo 19 `hr.leave.type.requires_allocation` is a `fields.Boolean` (NOT the `"yes"/"no"` Selection that the allocation task's cookbook claims); seed with `False`. `number_of_days` is working-day based, so Sunday (2026-05-10) -> Monday would yield 1 day; we use Monday -> Tuesday for a clean 2-day assert. State-diff ops on the new leave record are all `op: "create"`. |
