ROW: 356
TASK_ID: sale_purchase.mto_so_generate_po_change_vendor_confirm
DIFFICULTY: hard
SUMMARY: Seed a confirmed SO for an MTO+Buy storable product with two vendors; agent must follow SO -> Purchase smart-button to the auto-generated RFQ, swap its vendor from Acme Supply Co to Brook Trading Ltd (price_unit recomputes to 40), save, and Confirm the PO.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: under_target (both agents solved it on first try; explicit smart-button + vendor swap prompts removed expected ambiguity)

DETAIL_SECTION:
## sale_purchase.mto_so_generate_po_change_vendor_confirm

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Purchase, Stock (MTO + Buy via sale_purchase_stock bridge) |
| **Workflow** | Seed creates a confirmed SO for a storable product wired with MTO + Buy routes and two vendors (Acme 50.00 / Brook 40.00). Confirming the SO auto-generates a draft RFQ for Acme (first vendor by sequence). Agent opens the SO, clicks the Purchase smart button (reachable via `stock.reference.purchase_ids` when `sale_line_id` is not set on the PO line), changes `partner_id` to Brook Trading Ltd so `_compute_price_unit_and_date_planned_and_name` recomputes the line to 40.00, saves, and clicks Confirm Order. |
| **Capability tested** | Closed-loop cross-module navigation (Sales -> Purchase via smart button) + edit-the-generated-RFQ vs create-a-new-PO + vendor-driven price recompute. |
| **Notes** | Calibrated under target. Both oracle (24s) and browser-use (169s) passed cleanly — the prompt spells out the Purchase smart-button hop and the vendor swap explicitly. Could be escalated by hiding the smart-button hint or by seeding multiple RFQs (distractors). Seed had to (a) flip `stock.route_warehouse0_mto.active=True`, (b) flip `purchase_stock.route_warehouse0_buy.product_selectable=True`, (c) set `buy_to_resupply=True` on main warehouse and re-run `_create_or_update_route()`, and (d) force `procure_method='make_to_order'` on all MTO-route rules — otherwise `action_confirm` produces no RFQ. Also, in the MTO+Buy (non-dropship) flow the generated `purchase.order.line` does NOT carry `sale_line_id`; the SO<->PO link runs through `stock.reference.purchase_ids` (sale_purchase_stock override). Use `purchase.order.origin == SO.name` for check.py. |
