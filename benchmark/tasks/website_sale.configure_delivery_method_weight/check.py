"""Postcondition checks for website_sale.configure_delivery_method_weight."""


CARRIER_NAME = "Bench Weight Shipping"


def check(env):
    failures = []

    carriers = env["delivery.carrier"].with_context(active_test=False).search(
        [("name", "=", CARRIER_NAME)]
    )
    if not carriers:
        return [f"delivery.carrier '{CARRIER_NAME}' not found"]
    if len(carriers) > 1:
        failures.append(
            f"Expected exactly 1 delivery.carrier named '{CARRIER_NAME}',"
            f" found {len(carriers)}"
        )
    carrier = carriers[0]

    if not carrier.active:
        failures.append(f"Carrier '{CARRIER_NAME}' is archived; must be active")

    if carrier.delivery_type != "base_on_rule":
        failures.append(
            f"Carrier delivery_type is '{carrier.delivery_type}',"
            f" expected 'base_on_rule'"
        )

    # `is_published` is provided by website_sale via website.published.multi.mixin
    if not getattr(carrier, "is_published", False):
        failures.append(
            f"Carrier '{CARRIER_NAME}' is not published (is_published=True required)"
        )

    if not carrier.product_id:
        failures.append(
            f"Carrier '{CARRIER_NAME}' has no Delivery Product set"
        )

    rules = carrier.price_rule_ids
    if len(rules) != 2:
        failures.append(
            f"Expected exactly 2 delivery.price.rule rows on '{CARRIER_NAME}',"
            f" found {len(rules)}"
        )

    # Rule 1: weight <= 5 with list_base_price == 10
    low_rules = rules.filtered(
        lambda r: r.variable == "weight"
        and r.operator == "<="
        and abs(r.max_value - 5.0) < 0.01
    )
    if not low_rules:
        failures.append(
            "No price rule matching (variable=weight, operator='<=', max_value=5.0)"
            f" found; existing rules: {[(r.variable, r.operator, r.max_value, r.list_base_price, r.list_price) for r in rules]}"
        )
    else:
        rule = low_rules[0]
        if abs(rule.list_base_price - 10.0) > 0.01:
            failures.append(
                f"Low-weight rule list_base_price is {rule.list_base_price},"
                f" expected 10.0 (put the fixed fee in 'Sale Base Price', not 'Sale Price')"
            )
        if abs(rule.list_price - 0.0) > 0.01:
            failures.append(
                f"Low-weight rule list_price is {rule.list_price},"
                f" expected 0.0 (no per-kg multiplier)"
            )

    # Rule 2: weight > 5 with list_base_price == 20
    high_rules = rules.filtered(
        lambda r: r.variable == "weight"
        and r.operator == ">"
        and abs(r.max_value - 5.0) < 0.01
    )
    if not high_rules:
        failures.append(
            "No price rule matching (variable=weight, operator='>', max_value=5.0)"
            f" found; existing rules: {[(r.variable, r.operator, r.max_value, r.list_base_price, r.list_price) for r in rules]}"
        )
    else:
        rule = high_rules[0]
        if abs(rule.list_base_price - 20.0) > 0.01:
            failures.append(
                f"High-weight rule list_base_price is {rule.list_base_price},"
                f" expected 20.0 (fixed fee goes in 'Sale Base Price')"
            )
        if abs(rule.list_price - 0.0) > 0.01:
            failures.append(
                f"High-weight rule list_price is {rule.list_price}, expected 0.0"
            )

    return failures
