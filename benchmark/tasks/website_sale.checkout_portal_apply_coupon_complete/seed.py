"""Seed for website_sale.checkout_portal_apply_coupon_complete.

Closed-loop cross-module task that exercises the full public checkout
with a pre-generated coupon code:

    /shop -> product -> Add to cart -> /shop/cart (apply code)
          -> /shop/checkout or /shop/address -> /shop/payment
          -> Wire Transfer -> Pay now -> /shop/confirmation

The seed creates:
  - A published product `Bench Coupon Item` (list_price 100, no taxes).
  - A loyalty program `BENCH10` with program_type='coupons',
    discount_mode='percent', discount=10, applicability='order'.
  - Exactly ONE pre-generated `loyalty.card` with code `BENCH10CODE`
    linked to that program.
  - Wire Transfer as the only enabled payment provider (other providers
    are disabled so the /shop/payment radio is deterministic).
  - `sale.async_emails=True` so the SMTP-less ephemeral DB does NOT
    roll back the payment post-process cursor.
  - A complete billing address on admin's partner so /shop/address can
    be accepted with the default Save button.

Cleanup is child-first (payment.transaction -> account.move -> order
lines -> sale.order -> loyalty.card -> loyalty.program -> product) so
the seed is idempotent across re-runs.
"""

PRODUCT_NAME = "Bench Coupon Item"
PRODUCT_PRICE = 100.0

PROGRAM_NAME = "BENCH10"
COUPON_CODE = "BENCH10CODE"
DISCOUNT_PERCENT = 10.0


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup_prior_runs(env):
    admin = env.ref("base.user_admin")

    # Drop any prior sale.orders tied to our product or to admin's website cart.
    products = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    order_ids = set()
    if products:
        variant_ids = products.mapped("product_variant_ids").ids
        if variant_ids:
            ord_by_product = env["sale.order"].with_context(active_test=False).search([
                ("order_line.product_id", "in", variant_ids),
            ])
            order_ids.update(ord_by_product.ids)

    admin_drafts = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
    ])
    order_ids.update(admin_drafts.ids)

    if order_ids:
        orders = env["sale.order"].with_context(active_test=False).browse(list(order_ids)).exists()
        for order in orders:
            txs = env["payment.transaction"].search([("sale_order_ids", "in", order.id)])
            for tx in txs:
                try:
                    tx.sudo().unlink()
                except Exception:
                    pass
            for move in order.invoice_ids:
                if move.state == "posted":
                    try:
                        move.button_draft()
                    except Exception:
                        pass
                try:
                    move.button_cancel()
                except Exception:
                    pass
                try:
                    move.sudo().unlink()
                except Exception:
                    pass
            if order.state in ("sale", "done"):
                try:
                    order.with_context(disable_cancel_warning=True)._action_cancel()
                except Exception:
                    try:
                        order.action_cancel()
                    except Exception:
                        pass
            try:
                order.sudo().unlink()
            except Exception:
                pass

    # Drop prior coupon cards & program.
    prog = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    if prog:
        cards = env["loyalty.card"].with_context(active_test=False).search([
            ("program_id", "in", prog.ids),
        ])
        if cards:
            try:
                cards.sudo().unlink()
            except Exception:
                pass
        try:
            prog.write({"active": False})
            prog.sudo().unlink()
        except Exception:
            pass

    # Any stray coupon with our code (cross-program) — drop it too.
    stray = env["loyalty.card"].with_context(active_test=False).search([
        ("code", "=", COUPON_CODE),
    ])
    if stray:
        try:
            stray.sudo().unlink()
        except Exception:
            pass

    # Drop the product.
    if products:
        products.sudo().unlink()


def _enable_wire_transfer(env):
    provider = env.ref("payment.payment_provider_transfer", raise_if_not_found=False)
    if not provider:
        return
    provider.write({"state": "enabled", "is_published": True})


def _disable_competing_providers(env):
    transfer = env.ref("payment.payment_provider_transfer", raise_if_not_found=False)
    others = env["payment.provider"].search([
        ("state", "in", ("enabled", "test")),
    ])
    for provider in others:
        if transfer and provider.id == transfer.id:
            continue
        try:
            provider.write({"state": "disabled"})
        except Exception:
            pass


def _ensure_admin_address(env):
    admin = env.ref("base.user_admin")
    partner = admin.partner_id
    updates = {}
    us = env.ref("base.us")
    ca_state = env.ref("base.state_us_5")
    if not partner.country_id:
        updates["country_id"] = us.id
    if not partner.state_id:
        updates["state_id"] = ca_state.id
    if not partner.street:
        updates["street"] = "1 Bench Way"
    if not partner.city:
        updates["city"] = "San Francisco"
    if not partner.zip:
        updates["zip"] = "94105"
    if not partner.phone:
        updates["phone"] = "+1 555 0100"
    if not partner.email:
        updates["email"] = "admin@benchcoupon.test"
    if updates:
        partner.write(updates)


def setup(env):
    # 1. Required modules + async email ICP.
    _ensure_module(env, "website_sale")
    _ensure_module(env, "website_sale_loyalty")
    _ensure_module(env, "payment_custom")

    env["ir.config_parameter"].sudo().set_param("sale.async_emails", "True")

    # 2. Cleanup prior runs.
    _cleanup_prior_runs(env)

    # 3. Payment providers: enable only Wire Transfer.
    _enable_wire_transfer(env)
    _disable_competing_providers(env)

    # 4. Complete admin address for try_skip_step.
    _ensure_admin_address(env)

    # 5. Seed the product (published, untaxed, 100.0).
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": PRODUCT_PRICE,
        "is_published": True,
        "website_published": True,
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })

    # 6. Loyalty program `BENCH10`: program_type='coupons',
    #    discount_mode='percent', discount=10 on order.
    program = env["loyalty.program"].create({
        "name": PROGRAM_NAME,
        "program_type": "coupons",
        "applies_on": "current",
        "trigger": "with_code",
        "rule_ids": [(5, 0, 0), (0, 0, {
            "minimum_qty": 0,
            "minimum_amount": 0,
            # No code on the rule — code lives on the individual
            # loyalty.card for program_type='coupons'.
        })],
        "reward_ids": [(5, 0, 0), (0, 0, {
            "reward_type": "discount",
            "discount": DISCOUNT_PERCENT,
            "discount_mode": "percent",
            "discount_applicability": "order",
            "required_points": 1,
            "description": "10% off (BENCH10)",
        })],
    })

    # 7. One pre-generated coupon card with our fixed code.
    env["loyalty.card"].create({
        "program_id": program.id,
        "code": COUPON_CODE,
        "points": 1.0,
    })

    # 8. Website sanity.
    website = env["website"].search([], limit=1)
    if not website:
        raise RuntimeError("No website record present in DB; cannot run shop test")

    # 9. Seed-validation sanity.
    if tmpl.list_price != PRODUCT_PRICE:
        raise RuntimeError(
            f"Seed sanity failed: product list_price={tmpl.list_price}, expected {PRODUCT_PRICE}"
        )
    cards = env["loyalty.card"].search([("program_id", "=", program.id)])
    if len(cards) != 1 or cards.code != COUPON_CODE:
        raise RuntimeError(
            f"Seed sanity failed: loyalty cards={cards.mapped('code')},"
            f" expected exactly [{COUPON_CODE!r}]"
        )
