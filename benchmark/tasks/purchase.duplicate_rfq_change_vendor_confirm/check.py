"""Postcondition checks for purchase.duplicate_rfq_change_vendor_confirm.

Validates:
1. Original RFQ `BENCH-RFQ-DUP` still exists, still draft, still tied to
   Meridian Supply Co, still has its two product lines.
2. A new confirmed PO with partner_ref `PH-REISSUE-77` exists for vendor
   Pinnacle Hardware.
3. The duplicate's order deadline is 2026-05-28.
4. The new confirmed PO has the same two product lines with the same
   products, quantities, and prices.
5. No extra records under these references.
"""

from datetime import date, datetime, timedelta


def check(env):
    failures = []

    meridian = env["res.partner"].search(
        [("name", "=", "Meridian Supply Co")], limit=1
    )
    pinnacle = env["res.partner"].search(
        [("name", "=", "Pinnacle Hardware")], limit=1
    )
    if not meridian or not pinnacle:
        return ["Seed vendors not found"]

    original = env["purchase.order"].search(
        [("partner_ref", "=", "BENCH-RFQ-DUP")], limit=1
    )
    if not original:
        failures.append("Original RFQ 'BENCH-RFQ-DUP' is missing")
    else:
        if original.partner_id.id != meridian.id:
            failures.append(
                f"Original vendor is '{original.partner_id.display_name}', "
                "expected 'Meridian Supply Co'"
            )
        if original.state != "draft":
            failures.append(
                f"Original RFQ state is '{original.state}', expected 'draft'"
            )
        if len(original.order_line) != 2:
            failures.append(
                f"Original RFQ has {len(original.order_line)} lines, expected 2"
            )

    dup = env["purchase.order"].search(
        [("partner_ref", "=", "PH-REISSUE-77")], limit=1
    )
    if not dup:
        return failures + [
            "Duplicated PO with vendor reference 'PH-REISSUE-77' not found"
        ]

    if dup.partner_id.id != pinnacle.id:
        failures.append(
            f"Duplicate vendor is '{dup.partner_id.display_name}', "
            "expected 'Pinnacle Hardware'"
        )
    if dup.state != "purchase":
        failures.append(
            f"Duplicate state is '{dup.state}', expected 'purchase' (confirmed)"
        )
    if isinstance(dup.date_order, datetime):
        actual_date = (dup.date_order + timedelta(hours=8)).date()
    else:
        actual_date = dup.date_order
    if actual_date != date(2026, 5, 28):
        failures.append(
            f"Duplicate order deadline is {actual_date}, expected 2026-05-28"
        )

    lines = dup.order_line
    if len(lines) != 2:
        failures.append(
            f"Duplicate has {len(lines)} lines, expected 2"
        )
        return failures

    gasket = lines.filtered(lambda l: l.product_id.name == "Rubber Gasket")
    bolt = lines.filtered(lambda l: l.product_id.name == "Stainless Bolt M8")
    if not gasket:
        failures.append("Duplicate is missing the Rubber Gasket line")
    else:
        if gasket.product_qty != 200:
            failures.append(
                f"Duplicate Rubber Gasket qty is {gasket.product_qty}, expected 200"
            )
        if gasket.price_unit != 1.50:
            failures.append(
                f"Duplicate Rubber Gasket price is {gasket.price_unit}, expected 1.50"
            )
    if not bolt:
        failures.append("Duplicate is missing the Stainless Bolt M8 line")
    else:
        if bolt.product_qty != 500:
            failures.append(
                f"Duplicate Stainless Bolt M8 qty is {bolt.product_qty}, expected 500"
            )
        if bolt.price_unit != 0.75:
            failures.append(
                f"Duplicate Stainless Bolt M8 price is {bolt.price_unit}, expected 0.75"
            )

    extras = env["purchase.order"].search([
        ("partner_ref", "in", ["BENCH-RFQ-DUP", "PH-REISSUE-77"]),
    ])
    if len(extras) != 2:
        failures.append(
            f"Expected exactly 2 purchase orders across references, "
            f"found {len(extras)}"
        )

    return failures
