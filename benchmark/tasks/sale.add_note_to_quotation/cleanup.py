"""Clean up artifacts from previous runs."""


def cleanup(env):
    existing = env["sale.order"].search([("client_order_ref", "=", "BENCH-NOTE-01")])
    for so in existing:
        env["mail.message"].search([
            ("res_model", "=", "sale.order"),
            ("res_id", "=", so.id),
        ]).unlink()
    existing.unlink()