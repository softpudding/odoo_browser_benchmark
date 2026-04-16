"""Postcondition checks for purchase.reset_draft_edit_reconfirm."""


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", "Meridian Supply Co")], limit=1)
    if not vendor:
        return ["Vendor 'Meridian Supply Co' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
    ], limit=1)
    if not po:
        return ["Purchase order for 'Meridian Supply Co' not found"]

    if po.state != "purchase":
        failures.append(
            f"PO state is '{po.state}', expected 'purchase' (confirmed)"
        )

    expected_notes = "Updated via browser"
    actual_notes = (po.note or "").strip()
    if expected_notes not in actual_notes:
        failures.append(
            f"Terms and Conditions (note): expected '{expected_notes}', got '{actual_notes}'"
        )

    real_lines = [l for l in po.order_line if l.product_qty > 0 and l.product_id]
    if len(real_lines) != 1:
        failures.append(
            f"Expected exactly 1 order line, found {len(real_lines)}"
        )
    else:
        line = real_lines[0]
        if line.product_id.name != "Rubber Gasket":
            failures.append(
                f"Product: expected 'Rubber Gasket', got '{line.product_id.name}'"
            )
        if abs(line.product_qty - 100.0) > 0.01:
            failures.append(
                f"Quantity: expected 100, got {line.product_qty}"
            )
        if abs(line.price_unit - 1.50) > 0.01:
            failures.append(
                f"Unit price: expected 1.50, got {line.price_unit}"
            )

    return failures
