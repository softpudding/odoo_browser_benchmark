"""Postcondition checks for sale_loyalty.create_program_apply_reward_on_quotation."""


def check(env):
    failures = []

    program = env["loyalty.program"].search([("name", "=", "Harbor 15% Quotation Reward")], limit=1)
    if not program:
        return ["Loyalty program 'Harbor 15% Quotation Reward' not found"]

    if program.trigger != "with_code":
        failures.append(f"Program trigger is '{program.trigger}', expected 'with_code'")
    if program.program_type not in {"promo_code", "promotion", "coupons"}:
        failures.append(f"Unexpected program type '{program.program_type}'")
    if len(program.reward_ids) != 1:
        failures.append(f"Expected exactly 1 reward, found {len(program.reward_ids)}")
    else:
        reward = program.reward_ids[0]
        if reward.reward_type != "discount":
            failures.append(f"Reward type is '{reward.reward_type}', expected 'discount'")
        if abs(reward.discount - 15.0) > 0.0001:
            failures.append(f"Reward discount is {reward.discount}, expected 15.0")

    order = env["sale.order"].search([("client_order_ref", "=", "HARBOR-LOYALTY-01")], limit=1)
    if not order:
        failures.append("Target quotation not found")
        return failures

    reward_lines = order.order_line.filtered("is_reward_line")
    if len(reward_lines) != 1:
        failures.append(f"Expected exactly 1 reward line on the quotation, found {len(reward_lines)}")
    else:
        reward_line = reward_lines[0]
        if reward_line.reward_id.program_id.id != program.id:
            failures.append("Reward line is not linked to the created loyalty program")
        if reward_line.price_unit >= 0:
            failures.append("Reward line is not a discount line")

    return failures
