"""Clean up artifacts from previous runs."""


def cleanup(env):
    for ref in ("BENCH-SO-BACK", "BENCH-SO-BACK-DIST"):
        orders = env["sale.order"].search([
            ("client_order_ref", "=", ref),
        ])
        for so in orders:
            # Cancel and remove linked deliveries
            for picking in so.picking_ids:
                if picking.state not in ("cancel", "done"):
                    picking.action_cancel()
                picking.unlink()
            if so.state in ("sale", "done"):
                so._action_cancel()
            so.unlink()
