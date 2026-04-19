"""Postcondition checks for point_of_sale.refund_previous_order."""


CONFIG_NAME = "Bench Refund POS"
PRODUCT_NAME = "Bench Widget"
CASH_METHOD = "Bench Refund Cash"
ORIG_REF = "BENCH-REFUND-01"


def check(env):
    failures = []

    config = env["pos.config"].search([("name", "=", CONFIG_NAME)], limit=1)
    if not config:
        return [f"POS config '{CONFIG_NAME}' is missing"]

    sessions = env["pos.session"].search([("config_id", "=", config.id)])
    if not sessions:
        failures.append(f"No POS session exists for '{CONFIG_NAME}'")
    else:
        open_sessions = sessions.filtered(
            lambda s: s.state in {"opened", "opening_control"}
        )
        if not open_sessions:
            failures.append(
                f"POS session for '{CONFIG_NAME}' is not open anymore "
                f"(states={[s.state for s in sessions]})"
            )

    orders = env["pos.order"].search(
        [("config_id", "=", config.id)], order="id asc"
    )
    if len(orders) != 2:
        return failures + [
            f"Expected exactly 2 POS orders for '{CONFIG_NAME}' "
            f"(original + refund), found {len(orders)}"
        ]

    # Identify original and refund orders.
    orig = orders.filtered(lambda o: o.pos_reference == ORIG_REF)
    if len(orig) != 1:
        failures.append(
            f"Original order with pos_reference {ORIG_REF!r} not found uniquely"
        )
        return failures
    orig = orig[0]
    refund = (orders - orig)
    if len(refund) != 1:
        failures.append("Could not isolate refund order (expected 1 non-original)")
        return failures
    refund = refund[0]

    # Original order must still be paid/done/invoiced and unchanged.
    if orig.state not in {"paid", "done", "invoiced"}:
        failures.append(
            f"Original order state is '{orig.state}', expected paid/done/invoiced"
        )
    if abs(orig.amount_total - 30.0) > 0.01:
        failures.append(
            f"Original order amount_total is {orig.amount_total}, expected 30.0"
        )
    if len(orig.lines) != 1:
        failures.append(
            f"Original order expected 1 line, found {len(orig.lines)}"
        )
    else:
        oline = orig.lines[0]
        if abs(oline.qty - 3.0) > 0.0001:
            failures.append(
                f"Original order line qty is {oline.qty}, expected 3.0"
            )

    # Refund order must be paid, is_refund=True, single line at -1 * 10.
    if refund.state not in {"paid", "done", "invoiced"}:
        failures.append(
            f"Refund order state is '{refund.state}', expected paid/done/invoiced"
        )
    if not refund.is_refund:
        failures.append("Refund order is_refund is False, expected True")
    if abs(refund.amount_total - (-10.0)) > 0.05:
        failures.append(
            f"Refund order amount_total is {refund.amount_total}, expected -10.0"
        )

    if len(refund.lines) != 1:
        failures.append(
            f"Refund order expected 1 line, found {len(refund.lines)}"
        )
    else:
        rline = refund.lines[0]
        if rline.product_id.display_name != PRODUCT_NAME:
            failures.append(
                f"Refund line product is {rline.product_id.display_name!r}, "
                f"expected {PRODUCT_NAME!r}"
            )
        if abs(rline.qty - (-1.0)) > 0.0001:
            failures.append(
                f"Refund line qty is {rline.qty}, expected -1.0"
            )
        if abs(rline.price_unit - 10.0) > 0.01:
            failures.append(
                f"Refund line price_unit is {rline.price_unit}, expected 10.0"
            )
        if abs(rline.discount) > 0.01:
            failures.append(
                f"Refund line discount is {rline.discount}, expected 0.0"
            )
        if abs(rline.price_subtotal - (-10.0)) > 0.05:
            failures.append(
                f"Refund line price_subtotal is {rline.price_subtotal}, expected -10.0"
            )

    # Refund must have exactly one cash payment of -10.00.
    payments = refund.payment_ids
    if len(payments) != 1:
        failures.append(
            f"Refund expected 1 payment, found {len(payments)}"
        )
    else:
        p = payments[0]
        if p.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Refund payment method is '{p.payment_method_id.name}', "
                f"expected '{CASH_METHOD}'"
            )
        if abs(p.amount - (-10.0)) > 0.05:
            failures.append(
                f"Refund payment amount is {p.amount}, expected -10.0"
            )

    return failures
