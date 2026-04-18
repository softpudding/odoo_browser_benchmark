"""Postcondition checks for point_of_sale.add_item_apply_global_discount_pay_cash."""


CONFIG_NAME = "Bench Test Store"
PRODUCT_NAME = "Bench POS Widget"
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
        open_sessions = sessions.filtered(lambda s: s.state in {"opened", "opening_control"})
        if not open_sessions:
            failures.append(
                f"POS session for '{CONFIG_NAME}' is not open anymore (states={[s.state for s in sessions]})"
            )

    orders = env["pos.order"].search([("config_id", "=", config.id)])
    if len(orders) != 1:
        return failures + [
            f"Expected exactly 1 POS order for '{CONFIG_NAME}', found {len(orders)}"
        ]

    order = orders[0]
    if order.state not in {"paid", "done", "invoiced"}:
        failures.append(f"POS order state is '{order.state}', expected a paid order state")

    if abs(order.amount_total - 34.0) > 0.01:
        failures.append(
            f"POS order amount_total is {order.amount_total}, expected 34.0 (2 x 20.00 - 15%)"
        )

    widget_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_NAME
    )
    if len(widget_lines) != 1:
        failures.append(
            f"Expected exactly 1 order line for '{PRODUCT_NAME}', found {len(widget_lines)}"
        )
    else:
        widget_line = widget_lines[0]
        if abs(widget_line.qty - 2.0) > 0.0001:
            failures.append(f"'{PRODUCT_NAME}' qty is {widget_line.qty}, expected 2.0")
        if abs(widget_line.price_unit - 20.0) > 0.01:
            failures.append(
                f"'{PRODUCT_NAME}' price_unit is {widget_line.price_unit}, expected 20.0"
            )

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
            if disc_line.price_subtotal_incl > -5.5 or disc_line.price_subtotal_incl < -6.5:
                failures.append(
                    f"Discount line subtotal is {disc_line.price_subtotal_incl}, expected ~-6.0"
                )

    payments = order.payment_ids
    if len(payments) != 1:
        failures.append(f"Expected exactly 1 payment, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Payment method is '{payment.payment_method_id.name}', expected '{CASH_METHOD}'"
            )
        if abs(payment.amount - 34.0) > 0.01:
            failures.append(f"Payment amount is {payment.amount}, expected 34.0")

    return failures
