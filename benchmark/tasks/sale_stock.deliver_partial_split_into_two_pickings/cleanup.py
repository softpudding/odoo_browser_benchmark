"""Cleanup for sale_stock.deliver_partial_split_into_two_pickings.

Reverses what setup() created. Must handle every state the SO + its
pickings could be in after a failed/aborted run (draft, sale, done,
backordered, validated, etc.).
"""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "=", "S-BENCH-SPLIT-001"),
    ])
    for so in orders:
        for picking in so.picking_ids:
            child_bos = env["stock.picking"].search([
                ("backorder_id", "=", picking.id),
            ])
            for bo in child_bos:
                if bo.state not in ("cancel", "done"):
                    try:
                        bo.action_cancel()
                    except Exception:
                        pass
                try:
                    bo.unlink()
                except Exception:
                    pass
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass
            try:
                picking.unlink()
            except Exception:
                pass
        if so.state in ("sale", "done"):
            try:
                so._action_cancel()
            except Exception:
                pass
        try:
            so.unlink()
        except Exception:
            pass
