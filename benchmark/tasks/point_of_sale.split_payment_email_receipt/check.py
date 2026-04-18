"""Postcondition checks for point_of_sale.split_payment_email_receipt."""


def check(env):
    failures = []

    orders = env["pos.order"].search([("config_id.name", "=", "Benchmark Bistro")])
    if len(orders) != 1:
        return [f"Expected exactly 1 POS order for 'Benchmark Bistro', found {len(orders)}"]

    order = orders[0]
    if order.state not in {"paid", "done"}:
        failures.append(f"POS order state is '{order.state}', expected a paid or posted state")
    if order.partner_id.name != "Harbor Receipt Customer":
        failures.append("POS order is not linked to the expected customer")
    if order.email != "harbor.receipts@example.com":
        failures.append(f"Receipt email is '{order.email}', expected 'harbor.receipts@example.com'")

    lines = order.lines.filtered(lambda line: line.product_id.display_name == "Harbor Granola Box")
    if len(lines) != 1:
        failures.append(f"Expected exactly 1 order line for 'Harbor Granola Box', found {len(lines)}")

    payments = order.payment_ids.sorted("amount")
    if len(payments) != 2:
        failures.append(f"Expected exactly 2 payments, found {len(payments)}")
    else:
        payment_map = {payment.payment_method_id.name: payment.amount for payment in payments}
        if abs(payment_map.get("Bench Cash", 0.0) - 5.0) > 0.0001:
            failures.append(f"Bench Cash amount is {payment_map.get('Bench Cash')}, expected 5.0")
        if abs(payment_map.get("Bench Card", 0.0) - 4.6) > 0.0001:
            failures.append(f"Bench Card amount is {payment_map.get('Bench Card')}, expected 4.6")

    receipt_attachments = env["ir.attachment"].search([
        ("res_model", "=", "pos.order"),
        ("res_id", "=", order.id),
        ("name", "ilike", "Receipt-"),
    ])
    if not receipt_attachments:
        failures.append("No receipt attachment was created for the emailed order")

    return failures
