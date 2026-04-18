ROW: 322
TASK_ID: stock.create_putaway_rule_for_specific_category
DIFFICULTY: hard
SUMMARY: Create category-level putaway rule routing 'Bench Cold Items' from WH/Stock to WH/Stock/Refrigerator (non-default Category vs Product column)
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## stock.create_putaway_rule_for_specific_category

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS (F1=1.0, 0 postcondition failures, 109.3s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Inventory |
| **Workflow** | Navigate Inventory > Configuration > Putaway Rules; click New to add an inline editable row; fill location_in_id=WH/Stock, category_id=Bench Cold Items (NOT product_id), location_out_id=WH/Stock/Refrigerator; save the list. |
| **Capability tested** | Selecting the non-default Product Category column (not the default Product column) when both autocomplete fields are visible side-by-side and become mutually-readonly when one is set. |
| **Notes** | Calibrated as `hard` but BU passed first attempt with F1=1.0. The editable=bottom list view exposes both Product and Product Category columns; once the agent reads the prompt's explicit "Product Category" instruction, the choice is unambiguous and BU has no trouble. The mutual-readonly side-effect (filling category greys out product, and vice versa) actually HELPS BU because it makes the choice visually obvious. To make this genuinely hard, would need to combine with another non-default selection (e.g., a Storage Category dropdown that becomes required when sublocation='closest_location') or move to a wizard with radio buttons. |
