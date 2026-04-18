"""Seed for sale_loyalty.create_loyalty_program_apply_at_checkout.

Creates two published shop products and a draft web shop cart for the admin
user containing both products. Also seeds an unrelated distractor program
"Holiday Bonus 5%" that must remain untouched. The agent must:

1. Create a Discount Code loyalty program with a 10% order-discount reward,
   a $150 minimum purchase amount on the rule, and a reward description
   that matches the prompt exactly.
2. Navigate to /shop/cart and apply the new code so a discount line appears.
"""


PROGRAM_NAME = "Spring 10% Discount"
DISTRACTOR_NAME = "Holiday Bonus 5%"
CODE = "SPRING10"
DISTRACTOR_CODE = "HOL5"
PRODUCT_NAMES = ["Spring Lawn Chair", "Spring Garden Light"]
ORDER_REF = "SPRING-LOYAL-CART-01"


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
        ("name", "in", PRODUCT_NAMES),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    website = env["website"].search([], limit=1)
    if not website:
        raise RuntimeError("No website record present in DB")

    chair = env["product.template"].create({
        "name": PRODUCT_NAMES[0],
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 80.0,
        "is_published": True,
        "taxes_id": [(5, 0, 0)],
    })
    light = env["product.template"].create({
        "name": PRODUCT_NAMES[1],
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 40.0,
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
            "discount": 5,
            "discount_mode": "percent",
            "discount_applicability": "order",
            "required_points": 1,
            "description": "Holiday bonus reward",
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
        "product_id": chair.product_variant_id.id,
        "product_uom_qty": 2.0,
        "price_unit": 80.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": light.product_variant_id.id,
        "product_uom_qty": 1.0,
        "price_unit": 40.0,
        "tax_ids": [(5, 0, 0)],
    })

    if abs(order.amount_untaxed - 200.0) > 0.01:
        raise RuntimeError(
            f"Seed sanity failed: expected subtotal 200.0 got {order.amount_untaxed}"
        )
