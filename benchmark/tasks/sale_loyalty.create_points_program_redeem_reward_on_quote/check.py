"""Check sale_loyalty.create_points_program_redeem_reward_on_quote."""

def check(env):
    failures = []
    program = env["loyalty.program"].search([("name", "=", "Rotor Points Reward")], limit=1)
    if not program:
        return ["Program not found"]
    order = env["sale.order"].search([("client_order_ref", "=", "ROTOR-PTS-01")], limit=1)
    reward_lines = order.order_line.filtered("is_reward_line")
    if len(reward_lines) != 1:
        failures.append(f"Expected 1 reward line, found {len(reward_lines)}")
    else:
        if reward_lines[0].reward_id.program_id != program:
            failures.append("Reward line is not linked to the created program")
        if reward_lines[0].price_unit >= 0:
            failures.append("Reward line is not a discount line")
    return failures
