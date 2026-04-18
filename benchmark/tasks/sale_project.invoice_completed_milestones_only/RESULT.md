ROW: 307
TASK_ID: sale_project.invoice_completed_milestones_only
DIFFICULTY: hard
SUMMARY: Open SO S-BENCH-MS-002, click Create Invoice, accept wizard's auto-detected qty=2 (M1+M2 of 4 reached), Create Draft.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## sale_project.invoice_completed_milestones_only

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Project |
| **Workflow** | Open Sales app, find SO S-BENCH-MS-002 (Bench Quad Milestone Client, 1 line qty 4 of milestone-policy service). Click Create Invoice on the SO header. The wizard auto-fills line quantity 2 (M1+M2 of 4 milestones already reached). Accept Regular Invoice radio default and click Create Draft to land a draft account.move with 1 line qty=2, price 500, subtotal 1000. |
| **Capability tested** | Trust the Create Invoice wizard's auto-quantity for delivered_milestones products (do not override the line qty even though SO line qty is 4). |
| **Notes** | Calibration risk realized: browser-use solved this in 104s on the first run. The wizard's auto-detect is robust enough that agents accept it. To make this "hard" we'd need to add a non-default radio (Down Payment) or require typing a different qty — but the spec explicitly forbids both. The seed pre-marks M1+M2 reached so the agent doesn't even need to navigate to Project. With no wizard branching choice and no field entry, this is a single-button-click task once the agent finds the SO. SO line `invoice_status` flips to "no" (not "invoiced") because qty_to_invoice=0 and remaining undelivered units have not yet generated to_invoice flow. |
