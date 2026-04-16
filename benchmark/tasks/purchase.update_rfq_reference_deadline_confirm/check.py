"""Postcondition checks for purchase.update_rfq_reference_deadline_confirm."""

from datetime import date, datetime, timedelta


def check(env):
    failures = []

    vendor = env["res.partner"].search(
        [("name", "=", "North Coast Components")],
        limit=1,
    )
    if not vendor:
        return ["Vendor 'North Coast Components' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "MED-RFQ-REF-01"),
    ], limit=1)
    if not po:
        return ["Target RFQ 'MED-RFQ-REF-01' not found"]

    if po.state != "purchase":
        failures.append(f"PO state is '{po.state}', expected 'purchase'")
    if po.partner_ref != "NCC-8842":
        failures.append(
            f"Vendor Reference is '{po.partner_ref}', expected 'NCC-8842'"
        )

    if isinstance(po.date_order, datetime):
        # The UI date picker writes a midnight local date that is stored as UTC.
        actual_date = (po.date_order + timedelta(hours=8)).date()
    else:
        actual_date = po.date_order
    if actual_date != date(2026, 5, 22):
        failures.append(
            f"Order deadline is {actual_date}, expected 2026-05-22"
        )

    if len(po.order_line) != 1:
        failures.append(f"Expected 1 PO line, found {len(po.order_line)}")
        return failures

    dock_kit = po.order_line.filtered(lambda line: line.product_id.name == "Dock Seal Kit")

    if not dock_kit:
        failures.append("Dock Seal Kit line not found")
    else:
        if dock_kit.product_qty != 24:
            failures.append(
                f"Dock Seal Kit quantity is {dock_kit.product_qty}, expected 24"
            )
        if dock_kit.price_unit != 85.0:
            failures.append(
                f"Dock Seal Kit unit price is {dock_kit.price_unit}, expected 85.0"
            )

    distractor = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "MED-RFQ-REF-02"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor RFQ 'MED-RFQ-REF-02' not found")
    else:
        if distractor.state != "draft":
            failures.append(
                f"Distractor RFQ state is '{distractor.state}', expected 'draft'"
            )
        if distractor.partner_ref != "MED-RFQ-REF-02":
            failures.append(
                f"Distractor Vendor Reference is '{distractor.partner_ref}', expected 'MED-RFQ-REF-02'"
            )
        d_dock = distractor.order_line.filtered(
            lambda line: line.product_id.name == "Dock Seal Kit"
        )
        if d_dock and d_dock.product_qty != 18:
            failures.append(
                f"Distractor Dock Seal Kit quantity is {d_dock.product_qty}, expected 18"
            )

    return failures
