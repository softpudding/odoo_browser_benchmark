"""Cleanup for sale_purchase.dropship_so_to_po_chain_validate."""


SO_REF = "S-BENCH-DS-001"


def cleanup(env):
    so = env["sale.order"].search([("client_order_ref", "=", SO_REF)])
    for order in so:
        for picking in order.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
        linked_pos = env["purchase.order"].search([("origin", "=", order.name)])
        for po in linked_pos:
            for picking in po.picking_ids:
                if picking.state not in ("cancel", "done"):
                    picking.action_cancel()
            if po.state in ("purchase", "done"):
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()
        if order.state in ("sale", "done"):
            order._action_cancel()
        order.unlink()

    orphan_pos = env["purchase.order"].search([("origin", "=", SO_REF)])
    for po in orphan_pos:
        for picking in po.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()
