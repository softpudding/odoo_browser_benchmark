"""Postcondition checks for account.create_vendor_bill_confirm.

Validates:
1. Vendor bill exists with ref MSC-INV-4421
2. Bill is posted (state = posted)
3. Vendor is Meridian Supply Co
4. Bill date is 2026-05-01
5. Two invoice lines with correct products, quantities, prices
"""

from datetime import date


def check(env):
    failures = []

    bill = env["account.move"].search([
        ("ref", "=", "MSC-INV-4421"),
        ("move_type", "=", "in_invoice"),
    ], limit=1)

    if not bill:
        return ["Vendor bill with ref 'MSC-INV-4421' not found"]

    # Check state
    if bill.state != "posted":
        failures.append(f"Bill state is '{bill.state}', expected 'posted'")

    # Check vendor
    if bill.partner_id.name != "Meridian Supply Co":
        failures.append(
            f"Vendor is '{bill.partner_id.name}', expected 'Meridian Supply Co'"
        )

    # Check bill date
    expected_date = date(2026, 5, 1)
    if bill.invoice_date != expected_date:
        failures.append(
            f"Bill date is {bill.invoice_date}, expected {expected_date}"
        )

    # Check invoice lines (exclude tax/total lines)
    product_lines = bill.invoice_line_ids.filtered(
        lambda l: l.display_type == "product" or (not l.display_type and l.product_id)
    )

    if len(product_lines) != 2:
        failures.append(f"Expected 2 product lines, found {len(product_lines)}")
        return failures

    cable_line = product_lines.filtered(
        lambda l: l.product_id.name == "Cable Tray"
    )
    junction_line = product_lines.filtered(
        lambda l: l.product_id.name == "Junction Box"
    )

    if not cable_line:
        failures.append("Cable Tray line not found")
    else:
        if cable_line.quantity != 100:
            failures.append(
                f"Cable Tray qty is {cable_line.quantity}, expected 100"
            )
        if cable_line.price_unit != 12.50:
            failures.append(
                f"Cable Tray price is {cable_line.price_unit}, expected 12.50"
            )

    if not junction_line:
        failures.append("Junction Box line not found")
    else:
        if junction_line.quantity != 50:
            failures.append(
                f"Junction Box qty is {junction_line.quantity}, expected 50"
            )
        if junction_line.price_unit != 8.00:
            failures.append(
                f"Junction Box price is {junction_line.price_unit}, expected 8.00"
            )

    return failures
