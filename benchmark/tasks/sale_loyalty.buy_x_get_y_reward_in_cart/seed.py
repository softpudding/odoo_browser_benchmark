"""Seed for sale_loyalty.buy_x_get_y_reward_in_cart.

Creates two published shop products (Bench Widget, Bench Gadget) plus an
existing distractor loyalty program (must remain untouched). Also creates a
draft web shop cart for the admin user containing two Bench Widget units.

The agent must:
1. Create a 'promotion' loyalty program with a rule requiring qty 2 of the
   Bench Widget and a product reward giving 1 free Bench Gadget.
2. Navigate to /shop/cart where the auto-apply logic attaches a reward line
   for Bench Gadget with a zero price.
"""


PROGRAM_NAME = "Buy 2 Widgets Get 1 Gadget"
DISTRACTOR_NAME = "Winter Bundle 3%"
DISTRACTOR_CODE = "WINTER3"
BUY_PRODUCT_NAME = "Bench Widget"
REWARD_PRODUCT_NAME = "Bench Gadget"
ORDER_REF = "BXGY-WIDGET-CART-01"


def _cleanup(env):
    env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ]).sudo().unlink()
    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "in", [PROGRAM_NAME, DISTRACTOR_NAME]),
    ])
    if progs:
        progs.write({"active": False})
        progs.unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", [BUY_PRODUCT_NAME, REWARD_PRODUCT_NAME]),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    website = env["website"].search([], limit=1)
    if not website:
        raise RuntimeError("No website record present in DB")

    widget = env["product.template"].create({
        "name": BUY_PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 100.0,
        "is_published": True,
        "taxes_id": [(5, 0, 0)],
    })
    gadget = env["product.template"].create({
        "name": REWARD_PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 50.0,
        "is_published": True,
        "taxes_id": [(5, 0, 0)],
    })

    # Distractor existing loyalty program — agent must NOT modify it.
    env["loyalty.program"].create({
        "name": DISTRACTOR_NAME,
        "program_type": "promo_code",
        "applies_on": "current",
        "trigger": "with_code",
        "rule_ids": [(5, 0, 0), (0, 0, {
            "mode": "with_code",
            "code": DISTRACTOR_CODE,
            "minimum_qty": 0,
            "minimum_amount": 0,
        })],
        "reward_ids": [(5, 0, 0), (0, 0, {
            "reward_type": "discount",
            "discount": 3,
            "discount_mode": "percent",
            "discount_applicability": "order",
            "required_points": 1,
            "description": "Winter bundle reward",
        })],
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
        "product_id": widget.product_variant_id.id,
        "product_uom_qty": 2.0,
        "price_unit": 100.0,
        "tax_ids": [(5, 0, 0)],
    })

    if abs(order.amount_untaxed - 200.0) > 0.01:
        raise RuntimeError(
            f"Seed sanity failed: expected subtotal 200.0 got {order.amount_untaxed}"
        )
