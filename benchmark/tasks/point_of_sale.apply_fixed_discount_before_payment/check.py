"""Postcondition checks for point_of_sale.apply_fixed_discount_before_payment."""


CONFIG_NAME = "Bench POS"
PRODUCT_A_NAME = "Bench POS Item A"
PRODUCT_B_NAME = "Bench POS Item B"
CASH_METHOD = "Bench Cash"


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

    # Total should be ~30.00 (35 - 5).
    if abs(order.amount_total - 30.0) > 0.2:
        failures.append(
            f"POS order amount_total is {order.amount_total}, expected ~30.0 (35 - 14.29%)"
        )

    # Exactly one line for Item A at qty 1, price 20.
    a_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_A_NAME
    )
    if len(a_lines) != 1:
        failures.append(
            f"Expected exactly 1 order line for '{PRODUCT_A_NAME}', found {len(a_lines)}"
        )
    else:
        a_line = a_lines[0]
        if abs(a_line.qty - 1.0) > 0.0001:
            failures.append(f"'{PRODUCT_A_NAME}' qty is {a_line.qty}, expected 1.0")
        if abs(a_line.price_unit - 20.0) > 0.01:
            failures.append(
                f"'{PRODUCT_A_NAME}' price_unit is {a_line.price_unit}, expected 20.0"
            )

    # Exactly one line for Item B at qty 1, price 15.
    b_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_B_NAME
    )
    if len(b_lines) != 1:
        failures.append(
            f"Expected exactly 1 order line for '{PRODUCT_B_NAME}', found {len(b_lines)}"
        )
    else:
        b_line = b_lines[0]
        if abs(b_line.qty - 1.0) > 0.0001:
            failures.append(f"'{PRODUCT_B_NAME}' qty is {b_line.qty}, expected 1.0")
        if abs(b_line.price_unit - 15.0) > 0.01:
            failures.append(
                f"'{PRODUCT_B_NAME}' price_unit is {b_line.price_unit}, expected 15.0"
            )

    # Exactly one discount line using the configured discount product with a
    # price_subtotal ~ -5.00.
    discount_product = config.discount_product_id
    if discount_product:
        disc_lines = order.lines.filtered(
            lambda line: line.product_id.id == discount_product.id
        )
        if len(disc_lines) != 1:
            failures.append(
                f"Expected exactly 1 global discount line on the order, found {len(disc_lines)}"
            )
        else:
            disc_line = disc_lines[0]
            if disc_line.price_subtotal_incl > -4.5 or disc_line.price_subtotal_incl < -5.5:
                failures.append(
                    f"Discount line subtotal is {disc_line.price_subtotal_incl}, expected ~-5.0"
                )

    # Exactly one cash payment of ~30.0.
    payments = order.payment_ids
    if len(payments) != 1:
        failures.append(f"Expected exactly 1 payment, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Payment method is '{payment.payment_method_id.name}', expected '{CASH_METHOD}'"
            )
        if abs(payment.amount - 30.0) > 0.2:
            failures.append(f"Payment amount is {payment.amount}, expected ~30.0")

    return failures
