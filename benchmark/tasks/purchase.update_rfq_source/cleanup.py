"""Clean up artifacts from previous runs."""

VENDOR_NAME = "Horizon Components"


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return

    for src in ("BENCH-SRC-01", "BENCH-SRC-01-UPDATED"):
        env["purchase.order"].search([
            ("partner_id", "=", vendor.id),
            ("origin", "=", src),
        ]).unlink()
