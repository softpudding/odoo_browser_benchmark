"""Cleanup for purchase_stock.receive_partial_scrap_damaged_units."""

ORIGIN = "SCRAP-PO-07"
VENDOR_NAME = "Bench Harbor Supply"


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return
    orders = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", ORIGIN),
        ("state", "in", ["draft", "sent", "purchase"]),
    ])
    for order in orders:
        env["stock.scrap"].search([
            ("picking_id", "in", order.picking_ids.ids),
            ("state", "=", "draft"),
        ]).unlink()
        for picking in order.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            try:
                picking.action_cancel()
                picking.unlink()
            except Exception:
                pass
        try:
            if order.state == "purchase":
                order.button_cancel()
            if order.state == "cancel":
                order.button_draft()
            order.unlink()
        except Exception:
            pass
