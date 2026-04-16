"""Clean up artifacts from previous runs."""


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", "Nimbus Industrial Supply")], limit=1)
    if vendor:
        env["purchase.order"].search([
            ("partner_id", "=", vendor.id),
            ("origin", "=", "BENCH-CONFIRM-01"),
        ]).unlink()
