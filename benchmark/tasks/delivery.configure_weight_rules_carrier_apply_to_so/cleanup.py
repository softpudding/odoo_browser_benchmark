"""Cleanup for delivery.configure_weight_rules_carrier_apply_to_so."""


def cleanup(env):
    env["sale.order"].search([("client_order_ref", "=", "S-BENCH-DEL-001")]).unlink()
    env["delivery.carrier"].search([("name", "=", "Bench Weight Courier")]).unlink()
    env["product.template"].search([
        ("name", "in", ["Bench Weighted Widget", "Bench Shipping Charge"]),
    ]).unlink()
