"""Clean up artifacts from previous runs."""


ORIGIN = "P-BENCH-RET-001"


def cleanup(env):
    vendor = env["res.partner"].search(
        [("name", "=", "Bayside Components Co.")], limit=1
    )
    if not vendor:
        return

    orders = env["purchase.order"].search(
        [("partner_id", "=", vendor.id), ("origin", "=", ORIGIN)]
    )
    for po in orders:
        for picking in po.picking_ids:
            returns = env["stock.picking"].search([("return_id", "=", picking.id)])
            for ret in returns:
                if ret.state not in ("cancel", "done"):
                    ret.action_cancel()
                ret.move_ids.write({"state": "cancel"})
                ret.write({"state": "cancel"})
                ret.unlink()
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()
