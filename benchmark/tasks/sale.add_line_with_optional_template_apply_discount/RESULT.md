ROW: 324
TASK_ID: sale.add_line_with_optional_template_apply_discount
DIFFICULTY: medium
SUMMARY: Add new Bench Service Bundle line (qty=2, discount=10%) to draft SO S-BENCH-OPT-001 and save without confirming.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## sale.add_line_with_optional_template_apply_discount

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales |
| **Workflow** | Open seeded draft SO (customer reference S-BENCH-OPT-001, customer Bench Optional Co). Click "Add a product" in the order lines, pick "Bench Service Bundle" from the autocomplete, set qty=2 and per-line Discount=10 on that new row, then Save (do not Confirm). |
| **Capability tested** | Inline one2many row creation + per-row discount entry while leaving an existing line untouched. |
| **Notes** | Seed enables `sale.group_discount_per_so_line` so the Discount column renders on the line. "Bench Service Bundle" is a service product; "Bench Hardware Kit" is the pre-existing consumable line. Both Oracle (32s) and Browser-Use (143s) solved the task cleanly with F1=1.0 on first attempt, so the task calibrates EASIER than medium — the inline add+discount pattern is well within BU's current capability once the discount group is pre-enabled. No unauthorized writes, no forbidden ops. |
