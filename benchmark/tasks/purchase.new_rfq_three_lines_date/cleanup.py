"""Clean up artifacts from previous runs."""


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", "Meridian Supply Co")], limit=1)
    if not vendor:
        return
    pos = env["purchase.order"].search([("partner_id", "=", vendor.id)])
    for po in pos:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()
