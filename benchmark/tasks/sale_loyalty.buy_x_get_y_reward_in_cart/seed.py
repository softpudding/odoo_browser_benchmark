"""Seed for sale_loyalty.buy_x_get_y_reward_in_cart.

Seeds:
  * Customer 'Bench Promo Customer'
  * Product 'Bench Promo Widget' at €10.00 (no taxes)
  * Loyalty program 'Bench BOGO' (program_type='buy_x_get_y', trigger='auto',
    rule: min_qty=2 on Bench Promo Widget, reward: free qty=1 Bench Promo
    Widget, required_points=2)

Does NOT seed the sale.order. The agent must create a quotation with 2
widgets, claim the BOGO reward (deep UI interaction via the Coupons &
Promotions / reward wizard), and confirm the SO with 3 lines and
amount_total = 20.0.
"""


PROGRAM_NAME = "Bench BOGO"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Widget"


def _cleanup(env):
    # Orders first (references partner + product)
    partner = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CUSTOMER_NAME),
    ], limit=1)
    if partner:
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        if orders:
            confirmed = orders.filtered(lambda o: o.state not in ("draft", "cancel"))
            if confirmed:
                confirmed.sudo()._action_cancel()
            orders.sudo().unlink()

    # Loyalty program + cards
    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    if progs:
        env["loyalty.card"].with_context(active_test=False).search([
            ("program_id", "in", progs.ids),
        ]).sudo().unlink()
        progs.write({"active": False})
        progs.sudo().unlink()

    # Product template (drops variants and any stale orders referencing it)
    tmpl = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    if tmpl:
        # Any leftover order lines referencing the variant must be removed first
        variant_ids = tmpl.product_variant_ids.ids
        if variant_ids:
            leftover_lines = env["sale.order.line"].with_context(active_test=False).search([
                ("product_id", "in", variant_ids),
            ])
            if leftover_lines:
                leftover_orders = leftover_lines.order_id
                if leftover_orders:
                    confirmed = leftover_orders.filtered(
                        lambda o: o.state not in ("draft", "cancel")
                    )
                    if confirmed:
                        confirmed.sudo()._action_cancel()
                    leftover_orders.sudo().unlink()
        tmpl.sudo().unlink()

    # Partner
    if partner:
        partner.sudo().unlink()


def setup(env):
    _cleanup(env)

    partner = env["res.partner"].create({
        "name": CUSTOMER_NAME,
        "company_type": "person",
        "customer_rank": 1,
    })

    product_tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 10.0,
        "taxes_id": [(5, 0, 0)],
    })
    product = product_tmpl.product_variant_id

    program = env["loyalty.program"].create({
        "name": PROGRAM_NAME,
        "program_type": "buy_x_get_y",
        "trigger": "auto",
        "applies_on": "current",
        "active": True,
        "rule_ids": [(5, 0, 0), (0, 0, {
            "reward_point_mode": "unit",
            "product_ids": [(6, 0, [product.id])],
            "minimum_qty": 2,
        })],
        "reward_ids": [(5, 0, 0), (0, 0, {
            "reward_type": "product",
            "reward_product_id": product.id,
            "reward_product_qty": 1,
            "required_points": 2,
        })],
    })

    # Sanity
    if not program.active:
        raise RuntimeError("Seed sanity failed: program is not active")
    if program.program_type != "buy_x_get_y":
        raise RuntimeError(
            f"Seed sanity failed: program_type={program.program_type}"
        )
    if len(program.rule_ids) != 1 or len(program.reward_ids) != 1:
        raise RuntimeError(
            "Seed sanity failed: expected exactly 1 rule and 1 reward"
            f" (got {len(program.rule_ids)} rules, {len(program.reward_ids)} rewards)"
        )
    rule = program.rule_ids[0]
    if rule.minimum_qty != 2:
        raise RuntimeError(
            f"Seed sanity failed: rule.minimum_qty={rule.minimum_qty}, expected 2"
        )
    reward = program.reward_ids[0]
    if reward.reward_product_id != product:
        raise RuntimeError(
            "Seed sanity failed: reward product mismatch"
        )
    if reward.reward_product_qty != 1:
        raise RuntimeError(
            f"Seed sanity failed: reward_product_qty={reward.reward_product_qty}"
        )

    # Re-check the partner/product exist with expected attrs
    if partner.name != CUSTOMER_NAME:
        raise RuntimeError("Seed sanity failed: partner name mismatch")
    if abs(product_tmpl.list_price - 10.0) > 0.01:
        raise RuntimeError("Seed sanity failed: product list_price mismatch")
