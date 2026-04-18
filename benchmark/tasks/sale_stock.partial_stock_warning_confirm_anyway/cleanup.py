"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "=", "S-BENCH-STK-001"),
    ])
    for so in orders:
        for picking in so.picking_ids:
            # Cancel & remove backorder children first
            bo_children = env["stock.picking"].search([
                ("backorder_id", "=", picking.id),
            ])
            for bo in bo_children:
                if bo.state not in ("cancel", "done"):
                    bo.action_cancel()
                try:
                    bo.unlink()
                except Exception:
                    pass
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
            try:
                picking.unlink()
            except Exception:
                pass
        if so.state in ("sale", "done"):
            so._action_cancel()
        so.unlink()
