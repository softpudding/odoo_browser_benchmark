"""Seed for website_sale.apply_promo_code_at_checkout.

Seeds:
  * a simple partner 'Bench Promo Customer'
  * one product 'Bench Promo Product' (storable-less consu) priced at €100
  * a draft sale.order 'SO-BENCH-001' with one line for that product (qty 1,
    price 100, no taxes)

Does NOT seed the loyalty program - the agent must create it. Also cleans up
any prior Bench Promo program from earlier runs so we always start from a
blank slate.

Medium difficulty (Category 1 closed-loop cross-module): the agent must
configure a brand-new `program_type='promo_code'` loyalty.program with the
correct rule/reward fields, then switch to the Sales app to locate the
existing draft SO and apply the code. Getting either the program type or the
code field wrong breaks the second step.
"""


PROGRAM_NAME = "Bench Promo 10%"
PROMO_CODE = "BENCH10"
CUSTOMER_NAME = "Bench Promo Customer"
PRODUCT_NAME = "Bench Promo Product"
ORDER_REF = "SO-BENCH-001"


def _cleanup(env):
    # Orders first (references partner + product)
    orders = env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ])
    if orders:
        orders.filtered(lambda o: o.state not in ("draft", "cancel")).sudo().action_cancel()
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

    # Product + partner
    env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ]).sudo().unlink()
    env["res.partner"].with_context(active_test=False).search([
        ("name", "=", CUSTOMER_NAME),
    ]).sudo().unlink()


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
        "list_price": 100.0,
        "taxes_id": [(5, 0, 0)],
    })
    product = product_tmpl.product_variant_id

    order = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": ORDER_REF,
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": product.id,
        "product_uom_qty": 1.0,
        "price_unit": 100.0,
        "tax_ids": [(5, 0, 0)],
    })

    # Sanity
    if abs(order.amount_total - 100.0) > 0.01:
        raise RuntimeError(
            f"Seed sanity failed: expected order total 100.0 got {order.amount_total}"
        )
    if order.state != "draft":
        raise RuntimeError(
            f"Seed sanity failed: expected draft state got {order.state}"
        )
