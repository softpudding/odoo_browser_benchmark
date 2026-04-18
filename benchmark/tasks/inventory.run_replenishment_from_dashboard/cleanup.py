"""Cleanup for inventory.run_replenishment_from_dashboard."""

VENDOR_NAME = "Bench Supplies Ltd"
PRODUCT_NAME = "Bench Reorder Widget"


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        prior_pos = env["purchase.order"].search([("partner_id", "=", vendor.id)])
        for po in prior_pos:
            for pick in po.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            ):
                pick.action_cancel()
            if po.state in ("purchase", "done"):
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()

    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if products:
        env["stock.warehouse.orderpoint"].search([
            ("product_id", "in", products.ids)
        ]).unlink()
        env["stock.quant"].search([("product_id", "in", products.ids)]).unlink()
