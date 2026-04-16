"""Postcondition checks for purchase.update_rfq_source."""

VENDOR_NAME = "Horizon Components"
TARGET_SOURCE = "BENCH-SRC-01-UPDATED"
OLD_SOURCE = "BENCH-SRC-01"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    old = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", OLD_SOURCE),
    ], limit=1)
    if old:
        failures.append("RFQ source document was not updated")

    rfq = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", TARGET_SOURCE),
    ], limit=1)
    if not rfq:
        return [f"RFQ with source '{TARGET_SOURCE}' not found"]

    if rfq.state != "draft":
        failures.append(f"RFQ state is '{rfq.state}', expected 'draft'")

    if len(rfq.order_line) != 1:
        failures.append(f"Expected 1 line, found {len(rfq.order_line)}")

    return failures
