"""Cleanup for delivery.configure_fixed_rate_carrier_confirm_sale."""


def cleanup(env):
    env["sale.order"].search([("client_order_ref", "=", "HARBOR-SHIP-01")]).unlink()
    env["delivery.carrier"].search([("name", "=", "Harbor Flat Freight")]).unlink()
    env["product.template"].search([
        ("name", "in", ["Harbor Crate", "Harbor Flat Freight Service"]),
    ]).unlink()
