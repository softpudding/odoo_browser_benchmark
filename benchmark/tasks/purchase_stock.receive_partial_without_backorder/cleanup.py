"""Clean up artifacts from previous runs."""


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", "North Coast Components")], limit=1)
    if not vendor:
        return

    old_pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "NOBACK-04"),
    ])
    for po in old_pos:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()
