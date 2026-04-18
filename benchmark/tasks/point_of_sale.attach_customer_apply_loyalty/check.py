"""Postcondition checks for point_of_sale.attach_customer_apply_loyalty."""


CONFIG_NAME = "Bench Loyalty POS"
PRODUCT_NAME = "Bench POS Item"
CASH_METHOD = "Bench Loyalty Cash"
PROGRAM_NAME = "Bench Loyalty Program"
PARTNER_NAME = "Loyal Larry"


def check(env):
    failures = []

    config = env["pos.config"].search([("name", "=", CONFIG_NAME)], limit=1)
    if not config:
        return [f"POS config '{CONFIG_NAME}' is missing"]

    sessions = env["pos.session"].search([("config_id", "=", config.id)])
    if not sessions:
        failures.append(f"No POS session was opened for '{CONFIG_NAME}'")
    else:
        open_sessions = sessions.filtered(
            lambda s: s.state in {"opened", "opening_control"}
        )
        if not open_sessions:
            failures.append(
                f"POS session for '{CONFIG_NAME}' is not open anymore "
                f"(states={[s.state for s in sessions]})"
            )

    orders = env["pos.order"].search([("config_id", "=", config.id)])
    if len(orders) != 1:
        return failures + [
            f"Expected exactly 1 POS order for '{CONFIG_NAME}', found {len(orders)}"
        ]

    order = orders[0]

    if order.state not in {"paid", "done", "invoiced"}:
        failures.append(
            f"POS order state is '{order.state}', expected a paid order state"
        )

    # Customer must be Loyal Larry.
    if not order.partner_id:
        failures.append("POS order has no partner_id attached")
    elif order.partner_id.name != PARTNER_NAME:
        failures.append(
            f"POS order partner is '{order.partner_id.name}', expected '{PARTNER_NAME}'"
        )

    # Total should be 54.0 (60 - 10%).
    if abs(order.amount_total - 54.0) > 0.05:
        failures.append(
            f"POS order amount_total is {order.amount_total}, expected 54.0"
        )

    # Exactly one product line at qty 3.
    product_lines = order.lines.filtered(
        lambda line: line.product_id.display_name == PRODUCT_NAME and not line.is_reward_line
    )
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line for '{PRODUCT_NAME}', found {len(product_lines)}"
        )
    else:
        p_line = product_lines[0]
        if abs(p_line.qty - 3.0) > 0.0001:
            failures.append(f"'{PRODUCT_NAME}' qty is {p_line.qty}, expected 3.0")
        if abs(p_line.price_unit - 20.0) > 0.01:
            failures.append(
                f"'{PRODUCT_NAME}' price_unit is {p_line.price_unit}, expected 20.0"
            )

    # Exactly one reward line linked to the seeded program.
    program = env["loyalty.program"].search([("name", "=", PROGRAM_NAME)], limit=1)
    if not program:
        failures.append(f"Loyalty program '{PROGRAM_NAME}' is missing")
    else:
        reward_lines = order.lines.filtered(lambda l: l.is_reward_line)
        if len(reward_lines) != 1:
            failures.append(
                f"Expected exactly 1 reward line on the order, found {len(reward_lines)}"
            )
        else:
            r_line = reward_lines[0]
            if r_line.price_subtotal >= 0:
                failures.append(
                    f"Reward line subtotal is {r_line.price_subtotal}, expected negative"
                )
            if abs(r_line.price_subtotal + 6.0) > 0.5:
                failures.append(
                    f"Reward line subtotal is {r_line.price_subtotal}, expected approximately -6.0"
                )
            if r_line.reward_id and r_line.reward_id.program_id.id != program.id:
                failures.append(
                    "Reward line is not linked to the 'Bench Loyalty Program'"
                )

    # Payment: exactly one cash payment of 54.0.
    payments = order.payment_ids
    if len(payments) != 1:
        failures.append(f"Expected exactly 1 payment, found {len(payments)}")
    else:
        payment = payments[0]
        if payment.payment_method_id.name != CASH_METHOD:
            failures.append(
                f"Payment method is '{payment.payment_method_id.name}', expected '{CASH_METHOD}'"
            )
        if abs(payment.amount - 54.0) > 0.05:
            failures.append(f"Payment amount is {payment.amount}, expected 54.0")

    # The loyalty card should have been debited (or at least linked to the order).
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner and program:
        card = env["loyalty.card"].search(
            [("program_id", "=", program.id), ("partner_id", "=", partner.id)],
            limit=1,
        )
        if not card:
            failures.append(
                f"Loyalty card for '{PARTNER_NAME}' on '{PROGRAM_NAME}' was deleted"
            )
        else:
            # After redeeming a 50-point reward, the balance must have
            # decreased from the seeded 100 by at least the 50-point reward
            # cost. The POS order also awards 1 point for the earn-rule so a
            # typical final balance is 51 (100 + 1 - 50). Accept any value
            # strictly below the seeded 100 and at most 55 (allows for small
            # earn-rule variations if the agent tweaks quantities).
            if card.points >= 99.5:
                failures.append(
                    f"Loyalty card points is {card.points}, expected to have decreased "
                    f"after redeeming the 50-point reward"
                )
            if card.points > 55:
                failures.append(
                    f"Loyalty card points is {card.points}, expected approximately 51 "
                    f"(100 - 50 redeem + ~1 earn)"
                )

    return failures
