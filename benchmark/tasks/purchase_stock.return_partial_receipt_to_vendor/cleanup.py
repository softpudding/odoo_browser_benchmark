"""Clean up artifacts from previous runs."""


ORIGINS = ["RET-PO-07", "RET-PO-08"]


def cleanup(env):
    vendor = env["res.partner"].search(
        [("name", "=", "Harbor Precision Parts")], limit=1
    )
    if not vendor:
        return

    orders = env["purchase.order"].search(
        [("partner_id", "=", vendor.id), ("origin", "in", ORIGINS)]
    )
    for po in orders:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()
