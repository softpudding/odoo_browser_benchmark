"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", "Riverton Supply Co.")], limit=1)
    if partner:
        env["sale.order"].search([
            ("partner_id", "=", partner.id),
        ]).unlink()
