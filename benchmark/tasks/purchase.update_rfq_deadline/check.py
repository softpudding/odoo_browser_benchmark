"""Postcondition checks for purchase.update_rfq_deadline."""

VENDOR_NAME = "Horizon Components"
TARGET_DATE = "2026-05-20 00:00:00"
ORIGIN = "BENCH-RFQ-DEADLINE-01"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    rfq = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", ORIGIN),
    ], limit=1)
    if not rfq:
        return [f"RFQ '{ORIGIN}' for '{VENDOR_NAME}' not found"]

    actual_date = None
    if isinstance(rfq.date_order, str):
        actual_date = rfq.date_order
    else:
        actual_date = (
            rfq.date_order.strftime("%Y-%m-%d %H:%M:%S")
            if hasattr(rfq.date_order, "strftime")
            else str(rfq.date_order)
        )
    if actual_date != TARGET_DATE:
        failures.append(f"Order date is '{actual_date}', expected '{TARGET_DATE}'")

    if rfq.state != "draft":
        failures.append(f"RFQ state is '{rfq.state}', expected 'draft'")

    if len(rfq.order_line) != 1:
        failures.append(f"Expected 1 RFQ line, found {len(rfq.order_line)}")

    return failures
