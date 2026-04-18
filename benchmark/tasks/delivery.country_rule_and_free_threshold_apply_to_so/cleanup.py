"""Cleanup for delivery.country_rule_and_free_threshold_apply_to_so."""


def cleanup(env):
    env["sale.order"].search([
        ("client_order_ref", "in", ["SHIP-US-100", "SHIP-CA-100"]),
    ]).unlink()
    env["delivery.carrier"].search([
        ("name", "=", "US Harbor Freight"),
    ]).unlink()
    env["product.template"].search([
        ("name", "in", ["Bench Freight Item", "US Harbor Shipping"]),
    ]).unlink()
    env["res.partner"].search([
        ("name", "in", ["Bench US Customer", "Bench CA Customer"]),
    ]).unlink()
