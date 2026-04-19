ROW: 457
TASK_ID: stock.archive_old_product_set_inactive
DIFFICULTY: easy
SUMMARY: Archive storable product 'Bench Archive Me' via cog Actions menu; assert product.product.active=False AND product.template.active=False.
ORACLE: PASS (F1=1.0, 25.3s)
BROWSER_USE: PASS (F1=1.0, 86.3s single-shot)
F1: 1.0
CALIBRATION: matches (easy ~80% pass)

DETAIL_SECTION:
## stock.archive_old_product_set_inactive

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Inventory — Products |
| **Workflow** | Seed storable product Bench Archive Me (type='consu', is_storable=True, active=True). Agent: Inventory > Products > open Bench Archive Me > cog Actions > Archive. End state: product.template.active=False AND product.product.active=False. |
| **Capability tested** | Cog Actions menu Archive binding on product form — easy calibration anchor. |
| **Notes** | Archived records' active field emits norm_value=null (not false) in the diff engine because default active_test filters them out of post-task state capture. expected_state.json uses null accordingly. |
