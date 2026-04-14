"""Clean up artifacts from previous runs."""


def cleanup(env):
    for vendor_name in ["Atlas Industrial", "Pinnacle Parts"]:
        vendor = env["res.partner"].search([("name", "=", vendor_name)], limit=1)
        if vendor:
            pos = env["purchase.order"].search([("partner_id", "=", vendor.id)])
            for po in pos:
                for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
                    pick.action_cancel()
                if po.state in ("purchase", "done"):
                    po.button_cancel()
                if po.state == "cancel":
                    po.button_draft()
                po.unlink()
