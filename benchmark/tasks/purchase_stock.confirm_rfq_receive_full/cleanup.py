"""Cleanup for purchase_stock.confirm_rfq_receive_full."""


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", "Pioneer Industrial Supply")], limit=1)
    if not vendor:
        return
    orders = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "in", ["MED-RECV-PO-01", "MED-RECV-PO-02"]),
    ])
    for po in orders:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()
