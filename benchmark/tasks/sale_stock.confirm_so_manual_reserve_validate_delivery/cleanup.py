"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search(
        [("name", "=", "Bench SO Customer")], limit=1
    )
    if partner:
        orders = env["sale.order"].search([
            ("partner_id", "=", partner.id),
        ])
        for so in orders:
            for picking in so.picking_ids:
                if picking.state not in ("cancel", "done"):
                    picking.action_cancel()
                try:
                    picking.unlink()
                except Exception:
                    pass
            if so.state in ("sale", "done"):
                so._action_cancel()
            try:
                so.unlink()
            except Exception:
                pass
