"""Postcondition checks for sale_loyalty.buy_x_get_y_reward_in_cart."""


PROGRAM_NAME = "Bench BOGO"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Widget"
EXPECTED_TOTAL = 20.0
EXPECTED_UNIT_PRICE = 10.0


def check(env):
    failures = []

    # 1. Loyalty program must still exist, be active, and remain buy_x_get_y.
    program = env["loyalty.program"].with_context(active_test=False).search(
        [("name", "=", PROGRAM_NAME)], limit=1
    )
    if not program:
        return [f"Loyalty program '{PROGRAM_NAME}' not found"]
    if not program.active:
        failures.append(f"Loyalty program '{PROGRAM_NAME}' is archived")
    if program.program_type != "buy_x_get_y":
        failures.append(
            f"Program type is '{program.program_type}', expected 'buy_x_get_y'"
        )
    if len(program.reward_ids) != 1:
        failures.append(
            f"Expected exactly 1 reward on '{PROGRAM_NAME}',"
            f" found {len(program.reward_ids)}"
        )
    else:
        reward = program.reward_ids[0]
        if reward.reward_type != "product":
            failures.append(
                f"Reward type is '{reward.reward_type}', expected 'product'"
            )
        if reward.reward_product_qty != 1:
            failures.append(
                f"reward_product_qty is {reward.reward_product_qty}, expected 1"
            )
        if reward.required_points != 2:
            failures.append(
                f"required_points is {reward.required_points}, expected 2"
            )

    # 2. Seeded product must still exist at the expected price.
    product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return failures + [f"Seeded product '{PRODUCT_NAME}' not found"]
    if abs(product.lst_price - EXPECTED_UNIT_PRICE) > 0.01:
        failures.append(
            f"Product list_price is {product.lst_price},"
            f" expected {EXPECTED_UNIT_PRICE}"
        )

    # 3. Find the partner + order.
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not partner:
        return failures + [f"Seeded partner '{CUSTOMER_NAME}' not found"]

    orders = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", partner.id),
    ])
    if len(orders) != 1:
        return failures + [
            f"Expected exactly 1 sale.order for '{CUSTOMER_NAME}',"
            f" found {len(orders)} (names: {orders.mapped('name')})"
        ]
    order = orders

    if order.state != "sale":
        failures.append(
            f"Order state is '{order.state}', expected 'sale' (must be confirmed)"
        )

    if abs(order.amount_total - EXPECTED_TOTAL) > 0.05:
        failures.append(
            f"Order amount_total is {order.amount_total},"
            f" expected {EXPECTED_TOTAL}"
        )

    paid_lines = order.order_line.filtered(lambda l: not l.is_reward_line)
    reward_lines = order.order_line.filtered("is_reward_line")

    if len(paid_lines) != 1:
        failures.append(
            f"Expected exactly 1 paid (non-reward) line, found {len(paid_lines)}"
        )
    else:
        pline = paid_lines[0]
        if pline.product_id != product:
            failures.append(
                f"Paid line product is {pline.product_id.name!r},"
                f" expected {PRODUCT_NAME!r}"
            )
        if abs(pline.product_uom_qty - 2.0) > 0.01:
            failures.append(
                f"Paid line qty is {pline.product_uom_qty}, expected 2.0"
            )
        if abs(pline.price_unit - EXPECTED_UNIT_PRICE) > 0.01:
            failures.append(
                f"Paid line price_unit is {pline.price_unit},"
                f" expected {EXPECTED_UNIT_PRICE}"
            )

    if len(reward_lines) != 1:
        failures.append(
            f"Expected exactly 1 reward line, found {len(reward_lines)}"
        )
    else:
        rline = reward_lines[0]
        if rline.product_id != product:
            failures.append(
                f"Reward line product is {rline.product_id.name!r},"
                f" expected the Bench Promo Widget"
            )
        if abs(rline.product_uom_qty - 1.0) > 0.01:
            failures.append(
                f"Reward line qty is {rline.product_uom_qty}, expected 1.0"
            )
        if not rline.reward_id:
            failures.append("Reward line has no reward_id set")
        elif rline.reward_id.program_id.id != program.id:
            failures.append(
                "Reward line is not linked to the 'Bench BOGO' program"
                f" (linked to '{rline.reward_id.program_id.name}')"
            )
        # The reward line must net to ~0 on the order (100% discount).
        if abs(rline.price_subtotal) > 0.05:
            failures.append(
                f"Reward line price_subtotal is {rline.price_subtotal},"
                " expected ~0.0 (the free product should net to zero)"
            )

    return failures
