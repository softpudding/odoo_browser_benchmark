"""Seed for website_sale.add_optional_at_cart_remove_main_keep_optional.

Hard pattern: optional product orphaning. The shop is pre-configured with
'Bench Camera' (main, published) and 'Bench Tripod' (optional, published);
Bench Tripod is wired as an optional product of Bench Camera.

The agent must add Bench Camera to the cart, accept the Bench Tripod upsell
in the optional-products modal, then on /shop/cart click the trash icon on
the Bench Camera line ONLY -- leaving Bench Tripod orphaned in the cart.

We do NOT pre-seed the cart, so the agent must drive the website-shop
add-to-cart + optional-product modal flow themselves.
"""

ORDER_REF = "BENCH-OPT-ORPHAN-01"
MAIN_NAME = "Bench Camera"
OPTIONAL_NAME = "Bench Tripod"


def _cleanup(env):
    env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ]).sudo().unlink()
    # Also drop any draft website carts the admin may have left behind
    admin = env.ref("base.user_admin")
    env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
        ("state", "=", "draft"),
    ]).sudo().unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", [MAIN_NAME, OPTIONAL_NAME]),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    main = env["product.template"].create({
        "name": MAIN_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 320.0,
        "is_published": True,
        "website_published": True,
        "taxes_id": [(5, 0, 0)],
    })
    optional = env["product.template"].create({
        "name": OPTIONAL_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 75.0,
        "is_published": True,
        "website_published": True,
        "taxes_id": [(5, 0, 0)],
    })

    # Wire the optional accessory relationship so the website "Add to Cart"
    # button on Bench Camera shows Bench Tripod in the optional-product modal.
    main.write({
        "optional_product_ids": [(6, 0, [optional.id])],
    })

    # Sanity: must have a website to render /shop
    if not env["website"].search([], limit=1):
        raise RuntimeError("No website record present in DB; cannot run shop test")
