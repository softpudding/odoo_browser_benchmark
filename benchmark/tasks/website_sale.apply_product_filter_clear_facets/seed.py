"""Seed for website_sale.apply_product_filter_clear_facets.

Creates two website product categories and five published products:

    Gadgets
      Bench Gadget Mini  - 30
      Bench Gadget Plus  - 80
      Bench Gadget Pro   - 150
    Widgets
      Bench Widget Tiny  - 20
      Bench Widget Max   - 120

The agent's job is to use the /shop sidebar to filter first by Gadgets,
then by max_price=100, then CLEAR the category filter while keeping the
price filter active, and finally add 'Bench Widget Tiny' (the Widget
that is <= 100) to the cart. That sequence proves they understood the
two-way interaction between the category path filter and the price
query filter.
"""

CATEGORY_GADGETS = "Gadgets"
CATEGORY_WIDGETS = "Widgets"

GADGET_PRODUCTS = [
    ("Bench Gadget Mini", 30.0),
    ("Bench Gadget Plus", 80.0),
    ("Bench Gadget Pro", 150.0),
]
WIDGET_PRODUCTS = [
    ("Bench Widget Tiny", 20.0),
    ("Bench Widget Max", 120.0),
]
ALL_PRODUCT_NAMES = [n for n, _ in GADGET_PRODUCTS + WIDGET_PRODUCTS]
CATEGORY_NAMES = [CATEGORY_GADGETS, CATEGORY_WIDGETS]


def _cleanup(env):
    # Drop any leftover draft admin cart from a prior run.
    admin = env.ref("base.user_admin")
    env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
        ("state", "=", "draft"),
    ]).sudo().unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", ALL_PRODUCT_NAMES),
    ]).sudo().unlink()
    env["product.public.category"].with_context(active_test=False).search([
        ("name", "in", CATEGORY_NAMES),
    ]).sudo().unlink()


def setup(env):
    _cleanup(env)

    gadgets_cat = env["product.public.category"].create({
        "name": CATEGORY_GADGETS,
    })
    widgets_cat = env["product.public.category"].create({
        "name": CATEGORY_WIDGETS,
    })

    for name, price in GADGET_PRODUCTS:
        env["product.template"].create({
            "name": name,
            "type": "consu",
            "sale_ok": True,
            "purchase_ok": False,
            "list_price": price,
            "is_published": True,
            "website_published": True,
            "public_categ_ids": [(6, 0, [gadgets_cat.id])],
            "taxes_id": [(5, 0, 0)],
        })
    for name, price in WIDGET_PRODUCTS:
        env["product.template"].create({
            "name": name,
            "type": "consu",
            "sale_ok": True,
            "purchase_ok": False,
            "list_price": price,
            "is_published": True,
            "website_published": True,
            "public_categ_ids": [(6, 0, [widgets_cat.id])],
            "taxes_id": [(5, 0, 0)],
        })

    # Sanity: must have a website to render /shop
    if not env["website"].search([], limit=1):
        raise RuntimeError("No website record present in DB; cannot run shop test")
