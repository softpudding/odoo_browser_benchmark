"""Clean up artifacts from previous runs."""

VENDOR_NAME = "Horizon Components"
SOURCE = "BENCH-RFQ-DEADLINE-01"


def cleanup(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return

    env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", SOURCE),
    ]).unlink()
