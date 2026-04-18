"""Postcondition checks for website_sale.apply_promo_code_at_checkout."""


PROGRAM_NAME = "Bench Promo 10%"
PROMO_CODE = "BENCH10"
ORDER_REF = "SO-BENCH-001"
EXPECTED_SUBTOTAL = 100.0
EXPECTED_DISCOUNT = 10.0
EXPECTED_TOTAL = 90.0


def check(env):
    failures = []

    program = env["loyalty.program"].with_context(active_test=False).search(
        [("name", "=", PROGRAM_NAME)], limit=1
    )
    if not program:
        return [f"Loyalty program '{PROGRAM_NAME}' not found"]

    if not program.active:
        failures.append(f"Loyalty program '{PROGRAM_NAME}' exists but is archived")

    if program.program_type != "promo_code":
        failures.append(
            f"Program type is '{program.program_type}', expected 'promo_code'"
        )

    # Verify the rule carries the promo code
    code_rules = program.rule_ids.filtered(
        lambda r: (r.code or "").strip() == PROMO_CODE
    )
    if not code_rules:
        failures.append(
            f"No loyalty.rule with code '{PROMO_CODE}' found on program"
            f" '{PROGRAM_NAME}' (rules: {program.rule_ids.mapped('code')})"
        )
    else:
        rule = code_rules[0]
        if rule.mode != "with_code":
            failures.append(
                f"Rule for '{PROMO_CODE}' has mode='{rule.mode}', expected 'with_code'"
            )

    # Verify at least one discount reward at 10% on order
    reward_ok = program.reward_ids.filtered(
        lambda r: r.reward_type == "discount"
        and abs(r.discount - 10.0) < 0.01
        and r.discount_mode == "percent"
        and r.discount_applicability == "order"
    )
    if not reward_ok:
        rewards_desc = [
            f"(type={r.reward_type}, disc={r.discount}, mode={r.discount_mode},"
            f" applic={r.discount_applicability})"
            for r in program.reward_ids
        ]
        failures.append(
            "No reward matching reward_type=discount, discount=10,"
            f" discount_mode=percent, discount_applicability=order on program"
            f" '{PROGRAM_NAME}' (found: {rewards_desc})"
        )

    # Verify the seeded order
    order = env["sale.order"].with_context(active_test=False).search(
        [("client_order_ref", "=", ORDER_REF)], limit=1
    )
    if not order:
        return failures + [f"Seeded sale.order '{ORDER_REF}' not found"]

    if order.state != "draft":
        failures.append(
            f"Order state is '{order.state}', expected 'draft' (do not confirm)"
        )

    product_lines = order.order_line.filtered(lambda l: not l.is_reward_line)
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line on '{ORDER_REF}',"
            f" found {len(product_lines)}"
        )
    else:
        pline = product_lines[0]
        if abs(pline.product_uom_qty - 1.0) > 0.01:
            failures.append(
                f"Product line qty changed: {pline.product_uom_qty}, expected 1.0"
            )
        if abs(pline.price_unit - 100.0) > 0.01:
            failures.append(
                f"Product line price_unit changed: {pline.price_unit}, expected 100.0"
            )

    reward_lines = order.order_line.filtered("is_reward_line")
    if len(reward_lines) < 1:
        failures.append(
            "Expected at least 1 reward (discount) line on the order,"
            " found 0"
        )
    else:
        # The reward sum should be -10 (10% of 100)
        reward_total = sum(reward_lines.mapped("price_subtotal"))
        if reward_total >= 0:
            failures.append(
                f"Reward line total is {reward_total}, expected negative"
            )
        if abs(reward_total + EXPECTED_DISCOUNT) > 0.05:
            failures.append(
                f"Reward line total is {reward_total},"
                f" expected approximately {-EXPECTED_DISCOUNT}"
            )
        # At least one reward line should reference our program
        reward_programs = reward_lines.mapped("reward_id.program_id")
        if program.id not in reward_programs.ids:
            failures.append(
                f"No reward line references program '{PROGRAM_NAME}'"
                f" (found programs: {reward_programs.mapped('name')})"
            )

    if abs(order.amount_total - EXPECTED_TOTAL) > 0.05:
        failures.append(
            f"Order amount_total is {order.amount_total},"
            f" expected {EXPECTED_TOTAL}"
        )

    return failures
