"""Postcondition checks for purchase.new_rfq_three_lines_date.

Validates that a confirmed PO was created for Meridian Supply Co with
exactly three product lines (correct products, quantities, and prices)
and the correct Order Deadline date.
"""
import datetime


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", "Meridian Supply Co")], limit=1)
    if not vendor:
        return ["Vendor 'Meridian Supply Co' not found"]

    pos = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("state", "=", "purchase"),
    ])
    if not pos:
        failures.append("No confirmed Purchase Order found for Meridian Supply Co")
        return failures

    if len(pos) > 1:
        failures.append(
            f"Expected exactly 1 confirmed PO for Meridian Supply Co, found {len(pos)}"
        )
    po = pos[0]

    # Check Order Deadline (date_order is RFQ date; date_planned or individual line dates)
    # The "Order Deadline" in the Odoo UI is date_order on purchase.order in Odoo 19
    if po.date_order:
        order_date = po.date_order.date() if hasattr(po.date_order, 'date') else po.date_order
        expected_date = datetime.date(2026, 5, 30)
        if order_date != expected_date:
            failures.append(
                f"Order Deadline: expected 2026-05-30, got {order_date}"
            )
    else:
        failures.append("Order Deadline (date_order) is not set on the PO")

    # Filter out cancellation lines or zero-qty lines (empty phantom lines)
    real_lines = [l for l in po.order_line if l.product_qty > 0 and l.product_id]
    if len(real_lines) != 3:
        actual_names = [f"{l.product_id.name} x{l.product_qty}" for l in real_lines]
        failures.append(
            f"Expected exactly 3 product lines, found {len(real_lines)}: {actual_names}"
        )

    expected_lines = {
        "Rubber Gasket":     {"product_qty": 200.0, "price_unit": 1.50},
        "Stainless Bolt M8": {"product_qty": 500.0, "price_unit": 0.75},
        "Hex Nut M8":        {"product_qty": 500.0, "price_unit": 0.40},
    }
    found_names = set()
    for line in real_lines:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected product line: '{name}'")
            continue
        found_names.add(name)
        exp = expected_lines[name]
        if abs(line.product_qty - exp["product_qty"]) > 0.01:
            failures.append(
                f"Line '{name}': qty {line.product_qty}, expected {exp['product_qty']}"
            )
        if abs(line.price_unit - exp["price_unit"]) > 0.01:
            failures.append(
                f"Line '{name}': unit price {line.price_unit}, expected {exp['price_unit']}"
            )

    for name in expected_lines:
        if name not in found_names:
            failures.append(f"Missing product line: '{name}'")

    return failures
