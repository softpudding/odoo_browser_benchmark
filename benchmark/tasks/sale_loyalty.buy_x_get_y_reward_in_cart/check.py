"""Postcondition checks for sale_loyalty.buy_x_get_y_reward_in_cart."""


PROGRAM_NAME = "Buy 2 Widgets Get 1 Gadget"
DISTRACTOR_NAME = "Winter Bundle 3%"
DISTRACTOR_CODE = "WINTER3"
BUY_PRODUCT_NAME = "Bench Widget"
REWARD_PRODUCT_NAME = "Bench Gadget"
ORDER_REF = "BXGY-WIDGET-CART-01"
EXPECTED_SUBTOTAL = 200.0  # 2 * 100
EXPECTED_REWARD_QTY = 1.0


def check(env):
    failures = []

    program = env["loyalty.program"].search([("name", "=", PROGRAM_NAME)], limit=1)
    if not program:
        return [f"Loyalty program '{PROGRAM_NAME}' not found"]

    if not program.active:
        failures.append("Loyalty program exists but is archived")

    if program.program_type != "promotion":
        failures.append(
            f"Program type is '{program.program_type}', expected 'promotion'"
        )

    # --- Rule checks ---
    if len(program.rule_ids) != 1:
        failures.append(
            f"Expected exactly 1 rule on program, found {len(program.rule_ids)}"
        )
    else:
        rule = program.rule_ids[0]
        if rule.minimum_qty < 2:
            failures.append(
                f"Rule minimum_qty is {rule.minimum_qty}, expected >= 2"
            )
        rule_product_names = rule.product_ids.mapped("name")
        if BUY_PRODUCT_NAME not in rule_product_names:
            failures.append(
                f"Rule 'Among' product list is {rule_product_names},"
                f" must contain '{BUY_PRODUCT_NAME}'"
            )
        # Must not include the reward product in the qualifying list.
        if REWARD_PRODUCT_NAME in rule_product_names:
            failures.append(
                f"Rule 'Among' list wrongly contains reward product"
                f" '{REWARD_PRODUCT_NAME}'"
            )

    # --- Reward checks ---
    if len(program.reward_ids) != 1:
        failures.append(
            f"Expected exactly 1 reward on program, found {len(program.reward_ids)}"
        )
    else:
        reward = program.reward_ids[0]
        if reward.reward_type != "product":
            failures.append(
                f"Reward type is '{reward.reward_type}', expected 'product' (free product)"
            )
        if reward.reward_product_id.name != REWARD_PRODUCT_NAME and \
                REWARD_PRODUCT_NAME not in reward.reward_product_ids.mapped("name"):
            failures.append(
                f"Reward product is '{reward.reward_product_id.name}',"
                f" expected '{REWARD_PRODUCT_NAME}'"
            )
        if reward.reward_product_qty != EXPECTED_REWARD_QTY:
            failures.append(
                f"Reward product qty is {reward.reward_product_qty},"
                f" expected {EXPECTED_REWARD_QTY}"
            )

    # --- Distractor unchanged ---
    distractor = env["loyalty.program"].with_context(active_test=False).search(
        [("name", "=", DISTRACTOR_NAME)], limit=1
    )
    if not distractor:
        failures.append(f"Distractor program '{DISTRACTOR_NAME}' is missing (do not delete)")
    else:
        if not distractor.active:
            failures.append("Distractor program was archived")
        if DISTRACTOR_CODE not in distractor.rule_ids.mapped("code"):
            failures.append(
                f"Distractor rule code was modified: codes={distractor.rule_ids.mapped('code')}"
            )
        d_rewards = distractor.reward_ids
        if len(d_rewards) != 1 or abs(d_rewards.discount - 3.0) > 0.0001:
            failures.append(
                f"Distractor reward was modified: discount={d_rewards.mapped('discount')}"
            )

    # --- Cart checks ---
    order = env["sale.order"].search([("client_order_ref", "=", ORDER_REF)], limit=1)
    if not order:
        return failures + [f"Seeded shop cart '{ORDER_REF}' not found"]

    if order.state != "draft":
        failures.append(
            f"Cart state is '{order.state}', expected 'draft' (do not confirm/pay)"
        )

    product_lines = order.order_line.filtered(lambda l: not l.is_reward_line)
    widget_lines = product_lines.filtered(
        lambda l: l.product_id.product_tmpl_id.name == BUY_PRODUCT_NAME
    )
    if len(widget_lines) != 1 or widget_lines[0].product_uom_qty != 2.0:
        failures.append(
            f"Expected one {BUY_PRODUCT_NAME} line with qty=2 on cart,"
            f" found {widget_lines.mapped('product_uom_qty')}"
        )

    # The reward line MUST exist for Bench Gadget at price 0.
    reward_lines = order.order_line.filtered("is_reward_line")
    gadget_reward_lines = reward_lines.filtered(
        lambda l: l.product_id.product_tmpl_id.name == REWARD_PRODUCT_NAME
    )
    if not gadget_reward_lines:
        failures.append(
            f"Expected a reward line for '{REWARD_PRODUCT_NAME}' on the cart"
            f" — found reward lines: {reward_lines.mapped('product_id.name')}"
        )
    else:
        gline = gadget_reward_lines[0]
        # Free-product reward lines carry price_unit = list_price with
        # discount = 100%, so the line's effective (sub)total is 0.
        if abs(gline.price_subtotal) > 0.01:
            failures.append(
                f"Reward '{REWARD_PRODUCT_NAME}' line price_subtotal is"
                f" {gline.price_subtotal}, expected 0.0 (free product)"
            )
        if gline.product_uom_qty < 1.0:
            failures.append(
                f"Reward '{REWARD_PRODUCT_NAME}' line qty is {gline.product_uom_qty},"
                f" expected >= 1.0"
            )
        if gline.reward_id and program and gline.reward_id.program_id.id != program.id:
            failures.append(
                f"Reward line is linked to program '{gline.reward_id.program_id.name}',"
                f" expected '{PROGRAM_NAME}'"
            )

    return failures
