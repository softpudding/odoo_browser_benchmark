ROW: 329
TASK_ID: hr_holidays.bulk_approve_two_pending_requests
DIFFICULTY: hard
SUMMARY: Select exactly Eve's + Frank's pending leaves in Time Off manager list view, click bulk Approve, leave Alice's pending + distractor validated/refused leaves untouched.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.6667
CALIBRATION: matches

DETAIL_SECTION:
## hr_holidays.bulk_approve_two_pending_requests

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.6667 |
| **Odoo modules** | HR Holidays (Time Off) |
| **Workflow** | Navigate to `/odoo/time-off-approval`, switch to list view, clear default "Waiting For Me" facets, tick exactly the two checkboxes on Eve Pending's "Family vacation" row and Frank Pending's "Wedding attendance" row, then click the **Approve** bulk button that the `hr_holidays_payslip_list` JS controller renders in the list selection-actions slot. A third pending request (Alice Pending's "Personal errands") must stay in `confirm` state and two distractor leaves (one `validate`, one `refuse`) must be untouched. |
| **Capability tested** | Multi-record list selection combined with a non-generic bulk action button (not the built-in cog Actions menu; the custom `MultiRecordViewButton` shown by `HolidaysListController.displayButton`). Calibration trap: selecting all pending rows flips Alice's leave to `validate`, and approving each one individually violates the bulk-only instruction. |
| **Notes** | BU correctly flipped Eve + Frank to `validate` and kept Alice's state at `confirm` — but on the way it silently CREATED an extra `hr.leave` with `state='confirm'` (null name), dragging Strict down to FAIL. The task's postcondition `check.py` passed (all five canonical named records are in their expected states) while the state-diff engine counts the stray create as 2 unexpected extras, yielding Precision=0.5, Recall=1.0, F1=0.6667. Genuine hard-tier failure from the state-diff perspective. |
