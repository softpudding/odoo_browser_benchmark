ROW: 306
TASK_ID: purchase_stock.return_partial_with_distractor_lines
DIFFICULTY: hard
SUMMARY: Multi-line PO return wizard: zero out 2 distractor lines and set qty=2 on third, then validate return picking.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## purchase_stock.return_partial_with_distractor_lines

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Purchase, Stock |
| **Workflow** | Open seeded PO P-BENCH-RET-001 (3 lines, fully received), open the done receipt, click Return, set WidgetA=0, WidgetB=2, WidgetC=0 in the multi-line wizard, click Return, then Validate the new return picking. |
| **Capability tested** | Multi-line return wizard with selective per-row qty edits (2 distractor rows must be explicitly zeroed). |
| **Notes** | BU gave up at 480s with 0 successful steps; required op `stock.picking.button_validate` was missed and WidgetB qty stayed at 5. Calibration matches expected hardness — non-default attention test on auto-populated wizard rows. |
