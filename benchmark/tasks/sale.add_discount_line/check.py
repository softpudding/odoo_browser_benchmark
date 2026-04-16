"""Postcondition checks for sale.add_discount_line.

Validates:
1. Quotation BENCH-DISC-01 exists and is draft
2. Desk Organizer line has discount 10%
3. Monitor Stand line unchanged (0% discount)
"""

ORDER_REF = "BENCH-DISC-01"


def check(env):
    failures = []

    order = env["sale.order"].search([
        ("client_order_ref", "=", ORDER_REF),
    ], limit=1)

    if not order:
        return [f"Quotation with reference '{ORDER_REF}' not found"]

    if order.state != "draft":
        failures.append(f"Quotation state is '{order.state}', expected 'draft'")

    desk_line = order.order_line.filtered(lambda l: "Desk Organizer" in l.product_id.name)
    if not desk_line:
        failures.append("Desk Organizer line not found")
    elif desk_line.discount != 10.0:
        failures.append(f"Desk Organizer discount is {desk_line.discount}%, expected 10%")

    monitor_line = order.order_line.filtered(lambda l: "Monitor Stand" in l.product_id.name)
    if not monitor_line:
        failures.append("Monitor Stand line not found")
    elif monitor_line.discount != 0.0:
        failures.append(f"Monitor Stand discount changed to {monitor_line.discount}%, expected 0%")

    return failures