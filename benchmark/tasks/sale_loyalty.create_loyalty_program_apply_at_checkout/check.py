"""Postcondition checks for sale_loyalty.create_loyalty_program_apply_at_checkout."""


PROGRAM_NAME = "Spring 10% Discount"
DISTRACTOR_NAME = "Holiday Bonus 5%"
CODE = "SPRING10"
DISTRACTOR_CODE = "HOL5"
ORDER_REF = "SPRING-LOYAL-CART-01"
EXPECTED_REWARD_DESCRIPTION = "Spring Sale Discount"
EXPECTED_MIN_PURCHASE = 150.0
EXPECTED_SUBTOTAL = 200.0  # 2 * 80 + 1 * 40
EXPECTED_DISCOUNT_AMOUNT = 20.0  # 10% of 200


def check(env):
    failures = []

    program = env["loyalty.program"].search([("name", "=", PROGRAM_NAME)], limit=1)
    if not program:
        return [f"Loyalty program '{PROGRAM_NAME}' not found"]

    if not program.active:
        failures.append("Loyalty program exists but is archived")

    if program.program_type != "promo_code":
        failures.append(
            f"Program type is '{program.program_type}', expected 'promo_code'"
        )

    if len(program.reward_ids) != 1:
        failures.append(
            f"Expected exactly 1 reward on program, found {len(program.reward_ids)}"
        )
    else:
        reward = program.reward_ids[0]
        if reward.reward_type != "discount":
            failures.append(f"Reward type is '{reward.reward_type}', expected 'discount'")
        if reward.discount_mode != "percent":
            failures.append(
                f"Discount mode is '{reward.discount_mode}', expected 'percent'"
            )
        if abs(reward.discount - 10.0) > 0.0001:
            failures.append(f"Reward discount is {reward.discount}, expected 10.0")
        if reward.discount_applicability != "order":
            failures.append(
                f"Discount applicability is '{reward.discount_applicability}',"
                f" expected 'order'"
            )
        if (reward.description or "").strip() != EXPECTED_REWARD_DESCRIPTION:
            failures.append(
                f"Reward description is '{reward.description}',"
                f" expected '{EXPECTED_REWARD_DESCRIPTION}'"
            )

    code_rules = program.rule_ids.filtered(lambda r: (r.code or "").strip() == CODE)
    if not code_rules:
        failures.append(
            f"Program does not have a rule with code '{CODE}' — codes seen: {program.rule_ids.mapped('code')}"
        )
    else:
        rule = code_rules[0]
        if abs(rule.minimum_amount - EXPECTED_MIN_PURCHASE) > 0.01:
            failures.append(
                f"Rule minimum_amount is {rule.minimum_amount},"
                f" expected {EXPECTED_MIN_PURCHASE}"
            )

    # Distractor must remain unchanged.
    distractor = env["loyalty.program"].with_context(active_test=False).search(
        [("name", "=", DISTRACTOR_NAME)], limit=1
    )
    if not distractor:
        failures.append(f"Distractor program '{DISTRACTOR_NAME}' is missing (do not delete)")
    else:
        if not distractor.active:
            failures.append("Distractor program was archived")
        d_rewards = distractor.reward_ids
        if len(d_rewards) != 1 or abs(d_rewards.discount - 5.0) > 0.0001:
            failures.append(
                f"Distractor reward was modified: discount={d_rewards.mapped('discount')}"
            )
        if (DISTRACTOR_CODE not in distractor.rule_ids.mapped('code')):
            failures.append(
                f"Distractor rule code was modified: codes={distractor.rule_ids.mapped('code')}"
            )

    order = env["sale.order"].search([("client_order_ref", "=", ORDER_REF)], limit=1)
    if not order:
        return failures + [f"Seeded shop cart '{ORDER_REF}' not found"]

    if order.state != "draft":
        failures.append(
            f"Cart state is '{order.state}', expected 'draft' (do not confirm/pay)"
        )

    product_lines = order.order_line.filtered(lambda l: not l.is_reward_line)
    if len(product_lines) != 2:
        failures.append(
            f"Expected exactly 2 product lines on the cart, found {len(product_lines)}"
        )
    product_qty = sorted(product_lines.mapped("product_uom_qty"))
    if product_qty != [1.0, 2.0]:
        failures.append(
            f"Product line quantities changed: {product_qty}, expected [1.0, 2.0]"
        )

    reward_lines = order.order_line.filtered("is_reward_line")
    if len(reward_lines) != 1:
        failures.append(
            f"Expected exactly 1 reward/discount line on cart, found {len(reward_lines)}"
        )
    else:
        reward_line = reward_lines[0]
        if reward_line.reward_id.program_id.id != program.id:
            failures.append(
                "Reward line is not linked to the 'Spring 10% Discount' program"
            )
        if reward_line.price_subtotal >= 0:
            failures.append(
                f"Reward line subtotal is {reward_line.price_subtotal}, expected negative"
            )
        if abs(reward_line.price_subtotal + EXPECTED_DISCOUNT_AMOUNT) > 0.05:
            failures.append(
                f"Reward line amount is {reward_line.price_subtotal},"
                f" expected approximately {-EXPECTED_DISCOUNT_AMOUNT}"
            )

    expected_total = EXPECTED_SUBTOTAL - EXPECTED_DISCOUNT_AMOUNT
    if abs(order.amount_total - expected_total) > 0.05:
        failures.append(
            f"Cart amount_total is {order.amount_total}, expected {expected_total}"
        )

    return failures
