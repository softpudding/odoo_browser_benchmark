"""Postcondition checks for point_of_sale.close_session_reconcile_cash_diff."""


def check(env):
    failures = []

    session = env["pos.session"].search(
        [("config_id.name", "=", "Bench Close POS")], limit=1
    )
    if not session:
        return ["POS session for 'Bench Close POS' not found"]

    if session.state != "closed":
        failures.append(
            f"POS session state is {session.state!r}, expected 'closed'"
        )

    if abs(session.cash_register_balance_end_real - 97.0) > 1e-4:
        failures.append(
            f"cash_register_balance_end_real is {session.cash_register_balance_end_real}, expected 97.0"
        )

    if abs(session.cash_register_difference - (-3.0)) > 1e-4:
        failures.append(
            f"cash_register_difference is {session.cash_register_difference}, expected -3.0"
        )

    orders = env["pos.order"].search(
        [("config_id.name", "=", "Bench Close POS")]
    )
    if len(orders) != 1:
        failures.append(f"Expected exactly 1 POS order, found {len(orders)}")
    else:
        order = orders[0]
        if order.state not in {"paid", "done", "invoiced"}:
            failures.append(
                f"POS order state is {order.state!r}, expected paid/done/invoiced"
            )
        if abs(order.amount_total - 100.0) > 1e-4:
            failures.append(
                f"POS order amount_total is {order.amount_total}, expected 100.0"
            )
        payments = order.payment_ids
        if len(payments) != 1:
            failures.append(
                f"Expected exactly 1 payment on the order, found {len(payments)}"
            )
        elif payments[0].payment_method_id.name != "Bench Close Cash":
            failures.append(
                f"Payment method is {payments[0].payment_method_id.name!r}, expected 'Bench Close Cash'"
            )

    return failures
