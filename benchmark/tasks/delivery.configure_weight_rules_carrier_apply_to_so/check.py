"""Postcondition checks for delivery.configure_weight_rules_carrier_apply_to_so."""


def check(env):
    failures = []

    carrier = env["delivery.carrier"].search(
        [("name", "=", "Bench Weight Courier")], limit=1
    )
    if not carrier:
        return ["Delivery method 'Bench Weight Courier' not found"]

    if carrier.delivery_type != "base_on_rule":
        failures.append(
            f"Delivery type is '{carrier.delivery_type}', expected 'base_on_rule'"
        )

    rules = carrier.price_rule_ids
    if len(rules) < 2:
        failures.append(
            f"Expected at least 2 pricing rules on the carrier, found {len(rules)}"
        )
    else:
        # The 5kg/8.00 rule and 20kg/18.00 rule must both exist as weight rules.
        rule_5 = rules.filtered(
            lambda r: r.variable == "weight"
            and abs(r.max_value - 5.0) < 0.0001
            and abs(r.list_base_price - 8.0) < 0.0001
        )
        if not rule_5:
            failures.append(
                "Missing weight rule with max_value=5 and base price 8.00"
            )
        rule_20 = rules.filtered(
            lambda r: r.variable == "weight"
            and abs(r.max_value - 20.0) < 0.0001
            and abs(r.list_base_price - 18.0) < 0.0001
        )
        if not rule_20:
            failures.append(
                "Missing weight rule with max_value=20 and base price 18.00"
            )

    order = env["sale.order"].search(
        [("client_order_ref", "=", "S-BENCH-DEL-001")], limit=1
    )
    if not order:
        failures.append(
            "Target quotation with customer reference S-BENCH-DEL-001 not found"
        )
        return failures

    if order.state != "sale":
        failures.append(f"Order state is '{order.state}', expected 'sale'")
    if order.carrier_id.id != carrier.id:
        failures.append(
            f"Order delivery method is '{order.carrier_id.name or 'unset'}', "
            f"expected 'Bench Weight Courier'"
        )

    delivery_lines = order.order_line.filtered("is_delivery")
    if len(delivery_lines) != 1:
        failures.append(
            f"Expected exactly 1 delivery line, found {len(delivery_lines)}"
        )
    else:
        if abs(delivery_lines[0].price_unit - 8.0) > 0.0001:
            failures.append(
                f"Delivery line price is {delivery_lines[0].price_unit}, "
                f"expected 8.00 (the 5 kg rule should match)"
            )

    return failures
