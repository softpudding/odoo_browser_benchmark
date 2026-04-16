"""Postcondition checks for sale.confirm_order_within_credit_limit."""


def check(env):
    failures = []

    target = env["sale.order"].search(
        [("client_order_ref", "=", "CREDIT-OPS-07")], limit=1
    )
    distractor = env["sale.order"].search(
        [("client_order_ref", "=", "CREDIT-OPS-08")], limit=1
    )

    if not target:
        return ["Target quotation CREDIT-OPS-07 not found"]
    if not distractor:
        return ["Distractor quotation CREDIT-OPS-08 not found"]

    if target.state != "sale":
        failures.append(f"Target quotation state is {target.state!r}, expected 'sale'")

    expected_lines = {
        "Field Router Kit": {"qty": 3.0, "price": 400.0},
        "On-site Commissioning": {"qty": 1.0, "price": 1100.0},
    }
    for line in target.order_line.filtered(lambda l: l.product_id):
        exp = expected_lines.get(line.product_id.name)
        if exp is None:
            failures.append(f"Unexpected target line {line.product_id.name!r}")
            continue
        if abs(float(line.product_uom_qty or 0.0) - exp["qty"]) > 0.001:
            failures.append(
                f"{line.product_id.name} qty is {line.product_uom_qty}, expected {exp['qty']}"
            )
        if abs(float(line.price_unit or 0.0) - exp["price"]) > 0.001:
            failures.append(
                f"{line.product_id.name} unit price is {line.price_unit}, expected {exp['price']}"
            )

    if abs(float(target.amount_total or 0.0) - 2300.0) > 0.001:
        failures.append(f"Target quotation total is {target.amount_total}, expected 2300.0")

    if target.partner_credit_warning:
        failures.append("Target quotation still shows a partner credit warning")

    if distractor.state != "draft":
        failures.append(f"Distractor quotation state changed to {distractor.state!r}")

    distractor_lines = {
        "Field Router Kit": {"qty": 2.0, "price": 400.0},
        "On-site Commissioning": {"qty": 1.0, "price": 1100.0},
    }
    for line in distractor.order_line.filtered(lambda l: l.product_id):
        exp = distractor_lines.get(line.product_id.name)
        if exp is None:
            continue
        if abs(float(line.product_uom_qty or 0.0) - exp["qty"]) > 0.001:
            failures.append(
                f"Distractor line {line.product_id.name} qty changed to {line.product_uom_qty}"
            )
        if abs(float(line.price_unit or 0.0) - exp["price"]) > 0.001:
            failures.append(
                f"Distractor line {line.product_id.name} price changed to {line.price_unit}"
            )

    return failures
