"""Check delivery.configure_carrier_margin_rule_apply_to_order."""

def check(env):
    failures = []
    carrier = env["delivery.carrier"].search([("name", "=", "Bench Margin Courier")], limit=1)
    if not carrier:
        return ["Carrier not found"]
    if abs(carrier.fixed_margin - 6.0) > 0.0001:
        failures.append(f"fixed_margin is {carrier.fixed_margin}, expected 6.0")
    rule = carrier.price_rule_ids[:1]
    if not rule:
        failures.append("No pricing rule found")
    else:
        if abs(rule.list_base_price - 12.0) > 0.0001:
            failures.append(f"Base price is {rule.list_base_price}, expected 12.0")
    order = env["sale.order"].search([("client_order_ref", "=", "MARGIN-DEL-01")], limit=1)
    if order.state != "sale":
        failures.append(f"Order state is {order.state!r}, expected 'sale'")
    dlines = order.order_line.filtered("is_delivery")
    if len(dlines) != 1:
        failures.append(f"Expected 1 delivery line, found {len(dlines)}")
    elif abs(dlines[0].price_unit - 18.0) > 0.0001:
        failures.append(f"Delivery line price is {dlines[0].price_unit}, expected 18.0")
    return failures
