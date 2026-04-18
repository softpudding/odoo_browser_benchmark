"""Postcondition checks for point_of_sale.sell_two_products_apply_discount."""


CONFIG_NAME = "Bench Discount POS"
PRODUCT_PEN = "Bench POS Pen"
PRODUCT_NOTEBOOK = "Bench POS Notebook"
CASH_METHOD = "Bench Discount Cash"


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

    # Total should be 28.00 (10 + 18).
    if abs(order.amount_total - 28.0) > 0.05:
        failures.append(
            f"POS order amount_total is {order.amount_total}, expected 28.0"
        )

    # Pen line: qty 1, price 10, no discount.
    pen_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_PEN
    )
    if len(pen_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line for '{PRODUCT_PEN}', found {len(pen_lines)}"
        )
    else:
        p_line = pen_lines[0]
        if abs(p_line.qty - 1.0) > 0.0001:
            failures.append(f"'{PRODUCT_PEN}' qty is {p_line.qty}, expected 1.0")
        if abs(p_line.price_unit - 10.0) > 0.01:
            failures.append(
                f"'{PRODUCT_PEN}' price_unit is {p_line.price_unit}, expected 10.0"
            )
        if abs(p_line.discount) > 0.01:
            failures.append(
                f"'{PRODUCT_PEN}' discount is {p_line.discount}, expected 0.0 "
                f"(the discount must be on the Notebook line only)"
            )

    # Notebook line: qty 1, price 20, discount 10%.
    notebook_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_NOTEBOOK
    )
    if len(notebook_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line for '{PRODUCT_NOTEBOOK}', found {len(notebook_lines)}"
        )
    else:
        n_line = notebook_lines[0]
        if abs(n_line.qty - 1.0) > 0.0001:
            failures.append(f"'{PRODUCT_NOTEBOOK}' qty is {n_line.qty}, expected 1.0")
        if abs(n_line.price_unit - 20.0) > 0.01:
            failures.append(
                f"'{PRODUCT_NOTEBOOK}' price_unit is {n_line.price_unit}, expected 20.0"
            )
        if abs(n_line.discount - 10.0) > 0.01:
            failures.append(
                f"'{PRODUCT_NOTEBOOK}' discount is {n_line.discount}, expected 10.0"
            )
        if abs(n_line.price_subtotal - 18.0) > 0.05:
            failures.append(
                f"'{PRODUCT_NOTEBOOK}' price_subtotal is {n_line.price_subtotal}, "
                f"expected 18.0 (20.00 - 10%)"
            )

    # Payment: exactly one cash payment of 28.0.
    payments = order.payment_ids
    if len(payments) != 1:
        failures.append(f"Expected exactly 1 payment, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Payment method is '{payment.payment_method_id.name}', expected '{CASH_METHOD}'"
            )
        if abs(payment.amount - 28.0) > 0.05:
            failures.append(f"Payment amount is {payment.amount}, expected 28.0")

    return failures
