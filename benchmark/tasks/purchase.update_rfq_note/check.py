"""Postcondition checks for purchase.update_rfq_note."""

import re

TARGET_VENDOR = "Apex Supply Co."


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", TARGET_VENDOR)], limit=1)
    if not vendor:
        return ["Vendor 'Apex Supply Co.' not found"]

    rfq = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "BENCH-NOTE-01"),
    ], limit=1)
    if not rfq:
        return ["RFQ with source 'BENCH-NOTE-01' not found"]

    if rfq.state != "draft":
        failures.append(f"RFQ state is '{rfq.state}', expected 'draft'")

    normalized_note = re.sub(r"<[^>]*>", "", (rfq.note or "")).strip()
    if normalized_note != "Verified supplier confirmation. Keep shipping date tight.":
        failures.append(
            f"Notes are '{(rfq.note or '').strip()}', "
            "expected 'Verified supplier confirmation. Keep shipping date tight.'"
        )

    if len(rfq.order_line) != 1:
        failures.append(f"Expected 1 order line, found {len(rfq.order_line)}")

    return failures
