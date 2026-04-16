"""Postcondition checks for account.update_vendor_bill_reference_post."""

from datetime import date


def _product_lines(bill):
    return bill.invoice_line_ids.filtered(
        lambda line: line.display_type == "product" or (not line.display_type and line.product_id)
    )


def check(env):
    failures = []

    bill = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("ref", "=", "MSC-8841"),
    ], limit=1)
    if not bill:
        return ["Vendor bill 'MSC-8841' not found"]

    if bill.partner_id.name != "Meridian Supply Co":
        failures.append(
            f"Vendor is '{bill.partner_id.name}', expected 'Meridian Supply Co'"
        )
    if bill.state != "posted":
        failures.append(f"Bill state is '{bill.state}', expected 'posted'")
    if bill.invoice_date != date(2026, 5, 6):
        failures.append(
            f"Bill date is {bill.invoice_date}, expected 2026-05-06"
        )

    lines = _product_lines(bill)
    if len(lines) != 2:
        failures.append(f"Expected 2 product lines, found {len(lines)}")
        return failures

    cable = lines.filtered(lambda line: line.product_id.name == "Cable Tray")
    junction = lines.filtered(lambda line: line.product_id.name == "Junction Box")

    if not cable:
        failures.append("Cable Tray line not found")
    else:
        if cable.quantity != 60:
            failures.append(
                f"Cable Tray quantity is {cable.quantity}, expected 60"
            )
        if cable.price_unit != 12.5:
            failures.append(
                f"Cable Tray unit price is {cable.price_unit}, expected 12.5"
            )

    if not junction:
        failures.append("Junction Box line not found")
    else:
        if junction.quantity != 50:
            failures.append(
                f"Junction Box quantity is {junction.quantity}, expected 50"
            )
        if junction.price_unit != 8.0:
            failures.append(
                f"Junction Box unit price is {junction.price_unit}, expected 8.0"
            )

    distractor = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("ref", "=", "MED-VB-DRAFT-02"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor bill 'MED-VB-DRAFT-02' not found")
    else:
        if distractor.state != "draft":
            failures.append(
                f"Distractor bill state is '{distractor.state}', expected 'draft'"
            )
        lines = _product_lines(distractor)
        cable_line = lines.filtered(lambda line: line.product_id.name == "Cable Tray")
        if cable_line and cable_line.quantity != 40:
            failures.append(
                f"Distractor Cable Tray quantity is {cable_line.quantity}, expected 40"
            )

    return failures
