"""Postcondition checks for sale.cancel_confirmed_recreate_send_email.

Validates that the original SO is cancelled, a new quotation exists for
Clearwater Supply Co with the correct modified lines, and it was sent by email.
"""


def check(env):
    failures = []

    ironwood = env["res.partner"].search([("name", "=", "Ironwood Distribution")], limit=1)
    clearwater = env["res.partner"].search([("name", "=", "Clearwater Supply Co")], limit=1)
    if not ironwood or not clearwater:
        return ["Missing required customer partners"]

    # --- Original order must be cancelled ---
    old_order = env["sale.order"].search([
        ("partner_id", "=", ironwood.id),
        ("client_order_ref", "=", "BENCH-CANCEL-RESEND"),
    ], limit=1)
    if not old_order:
        failures.append("Original Ironwood Distribution order not found")
    elif old_order.state != "cancel":
        failures.append(
            f"Original order state is {old_order.state!r}, expected 'cancel'"
        )

    # --- New order for Clearwater Supply Co ---
    new_orders = env["sale.order"].search([
        ("partner_id", "=", clearwater.id),
        ("client_order_ref", "=", "CWS-REPLACE-01"),
    ])
    if not new_orders:
        failures.append("Replacement order for Clearwater Supply Co not found")
        return failures
    if len(new_orders) > 1:
        failures.append(f"Expected 1 replacement order, found {len(new_orders)}")

    new_order = new_orders[0]

    # Must be in "sent" state (email sent)
    if new_order.state != "sent":
        failures.append(
            f"Replacement order state is {new_order.state!r}, expected 'sent'"
        )

    # Check expiration date
    if str(new_order.validity_date) != "2026-07-15":
        failures.append(
            f"Expiration date is '{new_order.validity_date}', expected '2026-07-15'"
        )

    # Check order lines
    expected_lines = {
        "Heavy-Duty Shelf Unit":   {"product_uom_qty": 8.0,   "price_unit": 145.0},
        "Packing Tape Industrial": {"product_uom_qty": 200.0, "price_unit": 3.50},
    }

    product_lines = new_order.order_line.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
        and l.product_id
    )

    if len(product_lines) != 2:
        failures.append(
            f"Expected 2 product lines, found {len(product_lines)} "
            f"(products: {[l.product_id.name for l in product_lines]})"
        )

    for line in product_lines:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected product line: {name}")
            continue
        exp = expected_lines.pop(name)
        for field, val in exp.items():
            actual = getattr(line, field)
            if abs(actual - val) > 0.01:
                failures.append(
                    f"{name}.{field}: expected {val}, got {actual}"
                )

    for missing in expected_lines:
        failures.append(f"Missing product line: {missing}")

    # Ensure no extra SOs were created for Clearwater
    all_clearwater_orders = env["sale.order"].search([
        ("partner_id", "=", clearwater.id),
    ])
    if len(all_clearwater_orders) > 1:
        failures.append(
            f"Found {len(all_clearwater_orders)} orders for Clearwater Supply Co, expected 1"
        )

    return failures
