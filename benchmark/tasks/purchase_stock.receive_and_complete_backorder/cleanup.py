"""Clean up artifacts from previous runs."""


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", "Stellar Supplies")], limit=1)
    if vendor:
        pos = env["purchase.order"].search([
            ("partner_id", "=", vendor.id),
            ("origin", "=", "BENCH-PARTIAL"),
        ])
        for po in pos:
            for pick in po.picking_ids:
                if pick.state not in ("done", "cancel"):
                    pick.action_cancel()
            if po.state in ("purchase", "done"):
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()
