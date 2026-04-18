"""Cleanup for delivery.set_third_party_carrier_print_label."""


def cleanup(env):
    for so in env["sale.order"].search([("client_order_ref", "=", "S-BENCH-DLV-002")]):
        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
            picking.unlink()
        if so.state in ("sale", "done"):
            so._action_cancel()
        so.unlink()

    for picking in env["stock.picking"].search([("origin", "=", "S-BENCH-DLV-002")]):
        if picking.state not in ("cancel", "done"):
            picking.action_cancel()
        picking.unlink()

    env["delivery.carrier"].with_context(active_test=False).search([
        ("name", "=", "Bench Express"),
    ]).unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", ["Bench Express Crate", "Bench Express Shipping"]),
    ]).unlink()
