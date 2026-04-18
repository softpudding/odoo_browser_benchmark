"""Seed for website_sale.create_gift_card_apply_in_cart.

Seeds:
  * one published shop product (Spring Premium Bundle, €100)
  * a draft webshop cart for the admin user containing that product (subtotal €100)

Does NOT seed the loyalty program — the agent must create it. The default
`loyalty.gift_card_program` (Odoo's shipped demo) is left in place; the agent
must NOT touch it.

Hard pattern (Category 1 closed-loop cross-module): two-stage workflow that
mixes back-office configuration (program create + Generate Gift Cards wizard
+ copy code from smart button) with public-portal redemption (paste code into
/shop/cart). Browser-use frequently misses one of the wizard sub-steps or
applies the code on the back-office SO form instead of the cart.
"""


PROGRAM_NAME = "Spring Gift Card"
PRODUCT_NAME = "Spring Premium Bundle"
ORDER_REF = "SPRING-GIFTCARD-CART-01"


def _cleanup(env):
    env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ]).sudo().unlink()
    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    if progs:
        # cards must go before programs (ondelete=restrict on program_id)
        env["loyalty.card"].with_context(active_test=False).search([
            ("program_id", "in", progs.ids),
        ]).sudo().unlink()
        progs.write({"active": False})
        progs.unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    website = env["website"].search([], limit=1)
    if not website:
        raise RuntimeError("No website record present in DB")

    bundle = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 100.0,
        "is_published": True,
        "taxes_id": [(5, 0, 0)],
    })

    admin = env.ref("base.user_admin")
    partner = admin.partner_id

    order = env["sale.order"].create({
        "partner_id": partner.id,
        "website_id": website.id,
        "client_order_ref": ORDER_REF,
        "company_id": website.company_id.id,
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": bundle.product_variant_id.id,
        "product_uom_qty": 1.0,
        "price_unit": 100.0,
        "tax_ids": [(5, 0, 0)],
    })

    if abs(order.amount_untaxed - 100.0) > 0.01:
        raise RuntimeError(
            f"Seed sanity failed: expected subtotal 100.0 got {order.amount_untaxed}"
        )
