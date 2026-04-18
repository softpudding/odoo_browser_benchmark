ROW: 313
TASK_ID: mrp.scrap_component_during_partial_production
DIFFICULTY: hard
SUMMARY: Open MO, scrap 2 ScrewA via cog Actions->Scrap wizard with reason tag, then Produce All to finish 5 units.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## mrp.scrap_component_during_partial_production

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL (gave up at 480s; scrap_qty stayed at default 1.0) |
| **F1** | 0.0 |
| **Odoo modules** | Manufacturing |
| **Workflow** | Open confirmed MO M-BENCH-SCRAP-001, open the form's cog Actions menu and click Scrap, fill the wizard (product=ScrewA, qty=2, reason tag=Defective batch, source=WH/Stock), validate. Back on the MO, click Produce All / Mark As Done to finish 5 units of Bench Widget. |
| **Capability tested** | Discovering and using a binding server action exposed only through the form's cog Actions menu, then completing a multi-field wizard with a non-default quantity and a many2many tag, before finishing the MO. |
| **Notes** | Scrap action is a `binding_view_types="form"` server action (`mrp.action_production_order_scrap`) — it is NOT a header button, only available under the cog "Actions" dropdown. The wizard exposes `scrap_qty` (default 1.0) and `scrap_reason_tag_ids` (many2many of `stock.scrap.reason.tag`, no defaults seeded by Odoo). Seed creates the `Defective batch` reason tag and 40 units of stock for both components so reservation succeeds. Browser-Use validated a scrap successfully but left `scrap_qty` at the default 1.0 — exactly the calibration risk noted in the spec. Source-location field is hidden unless `stock.group_stock_multi_locations` is active, which is on in the base snapshot. |
