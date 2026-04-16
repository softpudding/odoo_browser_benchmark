"""Postcondition checks for sale.set_payment_terms_confirm.

Validates:
1. Quotation is confirmed (state = sale)
2. Payment terms set to "30 Net Days"
3. Customer reference is "AZ-2026-Q2"
4. Desk Organizer line quantity updated to 12
5. Monitor Stand line unchanged (qty 2, price 85)
6. No extra lines added or lines deleted
"""


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        return ["Partner 'Azure Interior' not found"]

    # Find the order — could have old or new ref
    so = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "in", ["AZ-2026-Q2", "BENCH-PMT-01"]),
    ], limit=1)
    if not so:
        return ["Sales order for Azure Interior not found"]

    # Check state
    if so.state != "sale":
        failures.append(f"Order state is '{so.state}', expected 'sale'")

    # Check customer reference
    if so.client_order_ref != "AZ-2026-Q2":
        failures.append(
            f"Customer reference is '{so.client_order_ref}', expected 'AZ-2026-Q2'"
        )

    # Check payment terms
    if not so.payment_term_id:
        failures.append("Payment terms not set")
    elif so.payment_term_id.name != "30 Net Days":
        failures.append(
            f"Payment terms is '{so.payment_term_id.name}', expected '30 Net Days'"
        )

    # Check order lines
    lines = so.order_line
    if len(lines) != 2:
        failures.append(f"Expected 2 order lines, found {len(lines)}")
        return failures

    desk_line = lines.filtered(lambda l: l.product_id.name == "Desk Organizer")
    monitor_line = lines.filtered(lambda l: l.product_id.name == "Monitor Stand")

    if not desk_line:
        failures.append("Desk Organizer line not found")
    else:
        if desk_line.product_uom_qty != 12:
            failures.append(
                f"Desk Organizer qty is {desk_line.product_uom_qty}, expected 12"
            )
        if desk_line.price_unit != 25.0:
            failures.append(
                f"Desk Organizer price is {desk_line.price_unit}, expected 25.0"
            )

    if not monitor_line:
        failures.append("Monitor Stand line not found")
    else:
        if monitor_line.product_uom_qty != 2:
            failures.append(
                f"Monitor Stand qty is {monitor_line.product_uom_qty}, expected 2"
            )
        if monitor_line.price_unit != 85.0:
            failures.append(
                f"Monitor Stand price is {monitor_line.price_unit}, expected 85.0"
            )

    return failures
