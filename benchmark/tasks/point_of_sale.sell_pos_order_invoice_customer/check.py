"""Postcondition checks for point_of_sale.sell_pos_order_invoice_customer."""


CONFIG_NAME = "Bench Invoice POS"
PRODUCT_NAME = "Bench Invoice Item"
CASH_METHOD = "Bench Invoice Cash"
PARTNER_NAME = "Invoice Iris"


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
            f"POS order state is '{order.state}', expected a paid/invoiced state"
        )

    if not order.partner_id:
        failures.append("POS order has no partner_id attached")
    elif order.partner_id.name != PARTNER_NAME:
        failures.append(
            f"POS order partner is '{order.partner_id.name}', expected '{PARTNER_NAME}'"
        )

    if abs(order.amount_total - 50.0) > 0.05:
        failures.append(
            f"POS order amount_total is {order.amount_total}, expected 50.0"
        )

    if not order.to_invoice:
        failures.append(
            "POS order to_invoice is False — agent did not enable the Invoice "
            "toggle on the payment screen, so no customer invoice was generated"
        )

    # Exactly one product line at qty 1.
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
        if abs(p_line.price_unit - 50.0) > 0.01:
            failures.append(
                f"'{PRODUCT_NAME}' price_unit is {p_line.price_unit}, expected 50.0"
            )

    # Payment: exactly one cash payment of 50.0.
    payments = order.payment_ids
    if len(payments) != 1:
        failures.append(f"Expected exactly 1 payment, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Payment method is '{payment.payment_method_id.name}', expected '{CASH_METHOD}'"
            )
        if abs(payment.amount - 50.0) > 0.05:
            failures.append(f"Payment amount is {payment.amount}, expected 50.0")

    # The whole point of the task: an account.move customer invoice must
    # have been created and posted, linked to Invoice Iris, for 50.00.
    move = order.account_move
    if not move:
        failures.append(
            "No account.move was generated — Invoice toggle was not active "
            "at validation time"
        )
    else:
        if move.state != "posted":
            failures.append(
                f"Generated account.move state is '{move.state}', expected 'posted'"
            )
        if move.move_type != "out_invoice":
            failures.append(
                f"Generated account.move type is '{move.move_type}', expected 'out_invoice'"
            )
        if not move.partner_id or move.partner_id.name != PARTNER_NAME:
            failures.append(
                f"Generated invoice partner is "
                f"'{move.partner_id.name if move.partner_id else None}', "
                f"expected '{PARTNER_NAME}'"
            )
        if abs(move.amount_total - 50.0) > 0.05:
            failures.append(
                f"Generated invoice amount_total is {move.amount_total}, expected 50.0"
            )

    return failures
