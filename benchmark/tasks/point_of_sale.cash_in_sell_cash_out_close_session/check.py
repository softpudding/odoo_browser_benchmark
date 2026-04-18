"""Postcondition checks for point_of_sale.cash_in_sell_cash_out_close_session."""


def check(env):
    failures = []

    session = env["pos.session"].search([("config_id.name", "=", "Benchmark Cash Desk")], limit=1)
    if not session:
        return ["POS session for 'Benchmark Cash Desk' not found"]

    if session.state != "closed":
        failures.append(f"POS session state is {session.state!r}, expected 'closed'")

    orders = env["pos.order"].search([("config_id.name", "=", "Benchmark Cash Desk")])
    if len(orders) != 1:
        failures.append(f"Expected exactly 1 POS order, found {len(orders)}")
    else:
        order = orders[0]
        if order.state not in {"paid", "done", "invoiced"}:
            failures.append(f"POS order state is {order.state!r}, expected paid/done/invoiced")
        lines = order.lines.filtered(lambda l: l.product_id.display_name == "Bench Snack Crate")
        if len(lines) != 1 or abs(lines[0].qty - 1.0) > 1e-4:
            failures.append("Expected one Bench Snack Crate line with qty 1")
        payments = order.payment_ids
        if len(payments) != 1:
            failures.append(f"Expected exactly 1 payment, found {len(payments)}")
        else:
            if payments[0].payment_method_id.name != "Bench Cash":
                failures.append(f"Payment method is {payments[0].payment_method_id.name!r}, expected 'Bench Cash'")
            if abs(payments[0].amount - 12.0) > 1e-4:
                failures.append(f"Payment amount is {payments[0].amount}, expected 12.0")

    statement_lines = session.statement_line_ids.sorted("amount")
    amounts = sorted(round(x, 2) for x in statement_lines.mapped("amount"))
    if 20.0 not in amounts:
        failures.append(f"Cash in line 20.0 not found in statement lines {amounts}")
    if -5.0 not in amounts:
        failures.append(f"Cash out line -5.0 not found in statement lines {amounts}")

    return failures
