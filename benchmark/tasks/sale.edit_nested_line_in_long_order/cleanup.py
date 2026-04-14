"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Summit Office Group")], limit=1)
    if partner:
        env["sale.order"].search([
            ("partner_id", "=", partner.id),
            ("client_order_ref", "=", "LONG-ORDER-01"),
        ]).unlink()
