"""Postcondition checks for point_of_sale.attach_customer_mid_sale."""


CONFIG_NAME = "Bench Easy POS"
PRODUCT_NAME = "Bench Easy POS Item"
CASH_METHOD = "Bench Easy Cash"
PARTNER_NAME = "Bench POS Easy Customer"


def check(env):
    failures = []

    config = env["pos.config"].search([("name", "=", CONFIG_NAME)], limit=1)
    if not config:
        return [f"POS config '{CONFIG_NAME}' is missing"]

    sessions = env["pos.session"].search([("config_id", "=", config.id)])
    if not sessions:
        failures.append(f"No POS session was opened for '{CONFIG_NAME}'")
    else:
        open_sessions = sessions.filtered(
            lambda s: s.state in {"opened", "opening_control"}
        )
        if not open_sessions:
            failures.append(
                f"POS session for '{CONFIG_NAME}' is not open anymore "
                f"(states={[s.state for s in sessions]})"
            )

    orders = env["pos.order"].search([("config_id", "=", config.id)])
    if len(orders) != 1:
        return failures + [
            f"Expected exactly 1 POS order for '{CONFIG_NAME}', found {len(orders)}"
        ]

    order = orders[0]

    if order.state not in {"paid", "done", "invoiced"}:
        failures.append(
            f"POS order state is '{order.state}', expected a paid order state"
        )

    # Customer must be the seeded customer.
    if not order.partner_id:
        failures.append("POS order has no partner_id attached")
    elif order.partner_id.name != PARTNER_NAME:
        failures.append(
            f"POS order partner is '{order.partner_id.name}', expected '{PARTNER_NAME}'"
        )

    # Total should be 15.0.
    if abs(order.amount_total - 15.0) > 0.05:
        failures.append(
            f"POS order amount_total is {order.amount_total}, expected 15.0"
        )

    # Exactly one product line for the seeded product.
    product_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_NAME
    )
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line for '{PRODUCT_NAME}', found {len(product_lines)}"
        )
    else:
        p_line = product_lines[0]
        if abs(p_line.qty - 1.0) > 0.0001:
            failures.append(f"'{PRODUCT_NAME}' qty is {p_line.qty}, expected 1.0")
        if abs(p_line.price_unit - 15.0) > 0.01:
            failures.append(
                f"'{PRODUCT_NAME}' price_unit is {p_line.price_unit}, expected 15.0"
            )

    # Payment: exactly one cash payment of 15.0.
    payments = order.payment_ids
    if len(payments) != 1:
        failures.append(f"Expected exactly 1 payment, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Payment method is '{payment.payment_method_id.name}', expected '{CASH_METHOD}'"
            )
        if abs(payment.amount - 15.0) > 0.05:
            failures.append(f"Payment amount is {payment.amount}, expected 15.0")

    return failures
