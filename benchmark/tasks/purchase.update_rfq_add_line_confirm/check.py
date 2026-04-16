"""Postcondition checks for purchase.update_rfq_add_line_confirm.

Validates:
1. PO is confirmed (state = purchase)
2. 3 order lines total (2 original + 1 new)
3. New line: Hex Wrench Set, qty 25, price 15.00
4. Original lines preserved unchanged
5. Order deadline is 2026-05-20
"""

from datetime import date, datetime


def check(env):
    failures = []

    vendor = env["res.partner"].search(
        [("name", "=", "Pinnacle Hardware")], limit=1
    )
    if not vendor:
        return ["Vendor 'Pinnacle Hardware' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", "BENCH-RFQ-UPD"),
    ], limit=1)

    if not po:
        return ["Purchase order with ref 'BENCH-RFQ-UPD' not found"]

    # Check state
    if po.state != "purchase":
        failures.append(f"PO state is '{po.state}', expected 'purchase'")

    # Check order deadline
    expected_deadline = date(2026, 5, 20)
    if po.date_order:
        actual_date = po.date_order.date() if isinstance(po.date_order, datetime) else po.date_order
        if actual_date != expected_deadline:
            failures.append(
                f"Order deadline is {actual_date}, expected {expected_deadline}"
            )

    # Check lines
    lines = po.order_line
    if len(lines) != 3:
        failures.append(f"Expected 3 order lines, found {len(lines)}")
        return failures

    # Check original lines preserved
    gasket = lines.filtered(lambda l: l.product_id.name == "Rubber Gasket")
    bolt = lines.filtered(lambda l: l.product_id.name == "Stainless Bolt M8")
    wrench = lines.filtered(lambda l: l.product_id.name == "Hex Wrench Set")

    if not gasket:
        failures.append("Rubber Gasket line missing")
    else:
        if gasket.product_qty != 200:
            failures.append(f"Rubber Gasket qty is {gasket.product_qty}, expected 200")

    if not bolt:
        failures.append("Stainless Bolt M8 line missing")
    else:
        if bolt.product_qty != 500:
            failures.append(f"Stainless Bolt M8 qty is {bolt.product_qty}, expected 500")

    if not wrench:
        failures.append("Hex Wrench Set line not found (new line not added)")
    else:
        if wrench.product_qty != 25:
            failures.append(f"Hex Wrench Set qty is {wrench.product_qty}, expected 25")
        if wrench.price_unit != 15.0:
            failures.append(f"Hex Wrench Set price is {wrench.price_unit}, expected 15.00")

    return failures
