"""Postcondition checks for website_sale.create_gift_card_apply_in_cart."""


PROGRAM_NAME = "Spring Gift Card"
ORDER_REF = "SPRING-GIFTCARD-CART-01"
EXPECTED_GIFT_CARD_VALUE = 50.0
EXPECTED_SUBTOTAL = 100.0
EXPECTED_DISCOUNT = 50.0
EXPECTED_TOTAL = 50.0
DEMO_GIFT_CARD_PROGRAM_NAME = "Gift Cards"


def check(env):
    failures = []

    program = env["loyalty.program"].search([("name", "=", PROGRAM_NAME)], limit=1)
    if not program:
        return [f"Loyalty program '{PROGRAM_NAME}' not found"]

    if not program.active:
        failures.append(f"Loyalty program '{PROGRAM_NAME}' exists but is archived")

    if program.program_type != "gift_card":
        failures.append(
            f"Program type is '{program.program_type}', expected 'gift_card'"
        )

    cards = env["loyalty.card"].with_context(active_test=False).search([
        ("program_id", "=", program.id),
    ])
    if len(cards) != 1:
        failures.append(
            f"Expected exactly 1 gift card on program '{PROGRAM_NAME}',"
            f" found {len(cards)}"
        )
    else:
        card = cards[0]
        if abs(card.points - EXPECTED_GIFT_CARD_VALUE) > 0.01:
            failures.append(
                f"Generated gift card has {card.points} points,"
                f" expected {EXPECTED_GIFT_CARD_VALUE}"
            )
        if not card.code:
            failures.append("Generated gift card has no code")

    # Default Odoo demo gift-card program must remain untouched.
    demo = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", DEMO_GIFT_CARD_PROGRAM_NAME),
        ("program_type", "=", "gift_card"),
    ], limit=1)
    if demo and not demo.active:
        failures.append(
            f"Default demo program '{DEMO_GIFT_CARD_PROGRAM_NAME}' was archived"
        )

    order = env["sale.order"].search([("client_order_ref", "=", ORDER_REF)], limit=1)
    if not order:
        return failures + [f"Seeded shop cart '{ORDER_REF}' not found"]

    if order.state != "draft":
        failures.append(
            f"Cart state is '{order.state}', expected 'draft' (do not confirm/pay)"
        )

    product_lines = order.order_line.filtered(lambda l: not l.is_reward_line)
    if len(product_lines) != 1:
        failures.append(
            f"Expected exactly 1 product line on the cart, found {len(product_lines)}"
        )
    else:
        if abs(product_lines.product_uom_qty - 1.0) > 0.01:
            failures.append(
                f"Product line qty changed: {product_lines.product_uom_qty},"
                f" expected 1.0"
            )

    reward_lines = order.order_line.filtered("is_reward_line")
    if len(reward_lines) != 1:
        failures.append(
            f"Expected exactly 1 reward (gift card payment) line,"
            f" found {len(reward_lines)}"
        )
    else:
        rline = reward_lines[0]
        rprogram = rline.reward_id.program_id
        if rprogram.id != program.id:
            failures.append(
                "Reward line program is not 'Spring Gift Card'"
                f" (got '{rprogram.name}')"
            )
        if rline.price_subtotal >= 0:
            failures.append(
                f"Reward line subtotal is {rline.price_subtotal}, expected negative"
            )
        if abs(rline.price_subtotal + EXPECTED_DISCOUNT) > 0.05:
            failures.append(
                f"Reward line amount is {rline.price_subtotal},"
                f" expected approximately {-EXPECTED_DISCOUNT}"
            )

    if abs(order.amount_total - EXPECTED_TOTAL) > 0.05:
        failures.append(
            f"Cart amount_total is {order.amount_total}, expected {EXPECTED_TOTAL}"
        )

    return failures
