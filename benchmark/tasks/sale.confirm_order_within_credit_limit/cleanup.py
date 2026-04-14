"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Northwind Electronics")], limit=1)
    if partner:
        env["sale.order"].search([
            ("partner_id", "=", partner.id),
            ("client_order_ref", "=", "CREDIT-CHECK-01"),
        ]).unlink()
