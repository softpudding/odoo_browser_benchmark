"""Postcondition checks for website_sale.checkout_portal_apply_coupon_complete."""

PRODUCT_NAME = "Bench Coupon Item"
PRODUCT_PRICE = 100.0

PROGRAM_NAME = "BENCH10"
COUPON_CODE = "BENCH10CODE"
DISCOUNT_PERCENT = 10.0

EXPECTED_TOTAL = 90.0
EXPECTED_PRODUCT_SUBTOTAL = 100.0
EXPECTED_DISCOUNT_AMOUNT = -10.0


def check(env):
    failures = []

    # ---- Program + coupon still consistent with seed. ----
    program = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ], limit=1)
    if not program:
        return [f"Seed broken: loyalty program '{PROGRAM_NAME}' missing"]
    if program.program_type != "coupons":
        failures.append(
            f"Program type is {program.program_type!r}, expected 'coupons'"
        )

    coupon = env["loyalty.card"].with_context(active_test=False).search([
        ("code", "=", COUPON_CODE),
    ], limit=1)
    if not coupon:
        failures.append(f"Coupon card '{COUPON_CODE}' missing")

    # ---- Locate admin's sale order (via the product). ----
    admin = env.ref("base.user_admin")
    products = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    if not products:
        return failures + [f"Seed broken: product '{PRODUCT_NAME}' missing"]
    variant_ids = products.mapped("product_variant_ids").ids

    orders = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
        ("order_line.product_id", "in", variant_ids),
    ])
    # Exclude cancelled orders so a stale seed-cleanup artefact is ignored.
    orders = orders.filtered(lambda o: o.state != "cancel")
    if not orders:
        return failures + [
            f"No sale.order found for admin containing '{PRODUCT_NAME}'"
        ]
    if len(orders) > 1:
        failures.append(
            f"Expected exactly 1 sale.order for admin containing "
            f"'{PRODUCT_NAME}', found {len(orders)}: {orders.mapped('name')}"
        )
    order = orders[0]

    # ---- Order state (Wire Transfer may leave it at 'sent'). ----
    if order.state not in ("sent", "sale", "done"):
        failures.append(
            f"sale.order state is {order.state!r}, expected 'sent', 'sale' or 'done'"
        )

    # ---- Order lines: 1 product + 1 reward discount line. ----
    # Delivery / shipping lines (is_delivery=True) are auto-added by
    # the shipping method picker; they are not "other products the
    # agent accidentally added" and must be excluded from the
    # extra-product-line check.
    def _is_delivery(line):
        return bool(getattr(line, "is_delivery", False))

    product_lines = order.order_line.filtered(
        lambda l: not l.is_reward_line and not _is_delivery(l)
    )
    reward_lines = order.order_line.filtered("is_reward_line")

    target_lines = product_lines.filtered(
        lambda l: l.product_id.product_tmpl_id.name == PRODUCT_NAME
    )
    if len(target_lines) != 1:
        failures.append(
            f"Expected exactly 1 '{PRODUCT_NAME}' product line, "
            f"found {len(target_lines)}: "
            f"{product_lines.mapped('product_id.display_name')}"
        )
    else:
        prod_line = target_lines[0]
        if abs(prod_line.product_uom_qty - 1.0) > 0.001:
            failures.append(
                f"'{PRODUCT_NAME}' qty is {prod_line.product_uom_qty}, expected 1"
            )
        if abs(prod_line.price_unit - PRODUCT_PRICE) > 0.01:
            failures.append(
                f"'{PRODUCT_NAME}' price_unit is {prod_line.price_unit},"
                f" expected {PRODUCT_PRICE}"
            )

    # No other (non-delivery, non-reward) product lines.
    non_target_products = product_lines - target_lines
    if non_target_products:
        failures.append(
            f"Unexpected extra product line(s) on cart: "
            f"{non_target_products.mapped('product_id.display_name')}"
        )

    # Exactly 1 reward line tied to the BENCH10 program.
    bench10_rewards = reward_lines.filtered(
        lambda l: l.reward_id.program_id.id == program.id
    )
    if len(bench10_rewards) != 1:
        failures.append(
            f"Expected exactly 1 reward line from '{PROGRAM_NAME}', "
            f"found {len(bench10_rewards)} "
            f"(all reward lines: {reward_lines.mapped('name')})"
        )
    else:
        rline = bench10_rewards[0]
        # A percent discount reward on a 100.0 order carries price_unit=-10.
        if abs(rline.price_subtotal - EXPECTED_DISCOUNT_AMOUNT) > 0.01:
            failures.append(
                f"Reward line price_subtotal is {rline.price_subtotal},"
                f" expected {EXPECTED_DISCOUNT_AMOUNT}"
            )

    # ---- Totals. ----
    if abs(order.amount_total - EXPECTED_TOTAL) > 0.01:
        failures.append(
            f"Order amount_total is {order.amount_total},"
            f" expected {EXPECTED_TOTAL}"
        )

    # ---- Payment transaction via Wire Transfer. ----
    txs = env["payment.transaction"].search([
        ("sale_order_ids", "in", order.id),
    ])
    if not txs:
        failures.append(
            f"No payment.transaction linked to sale.order {order.name!r}"
        )
    else:
        if not any(s in ("pending", "authorized", "done") for s in txs.mapped("state")):
            failures.append(
                f"Payment transaction state(s) are {txs.mapped('state')}, "
                f"expected at least one in ('pending','authorized','done')"
            )
        wire = env.ref(
            "payment.payment_provider_transfer", raise_if_not_found=False
        )
        if wire and not any(t.provider_id == wire for t in txs):
            failures.append(
                "No transaction uses the 'Wire Transfer' payment "
                "provider — agent likely paid with a different method"
            )

    return failures
