"""Seed for website_sale_stock.show_stock_availability_add_to_cart.

Installs ``website_sale_stock`` (bridge module, not in base snapshot) and
creates one storable product ``Bench Limited Stock`` with:

  - is_storable = True (Odoo 19: type='consu' + is_storable=True)
  - 5 units on-hand at WH/Stock
  - show_availability = True   (expose the "X in stock" banner)
  - available_threshold = 100  (keep the banner visible for any qty <= 100)
  - allow_out_of_stock_order = True (default; removes the sold-out gate
    so the agent can type arbitrary qty)
  - list_price = 40.0
  - is_published = True

The agent's task is to open the product on /shop, verify the stock
availability banner is rendered, and add 3 units to the admin cart.
"""


PRODUCT_NAME = "Bench Limited Stock"
LIST_PRICE = 40.0
STOCK_ON_HAND = 5.0
AVAILABLE_THRESHOLD = 100.0


def _ensure_website_sale_stock(env):
    """Install website_sale_stock + its deps if missing from base snapshot."""
    for mod_name in ("sale_stock", "stock_delivery", "website_sale_stock"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()


def _cleanup(env):
    admin = env.ref("base.user_admin")

    # Drop any leftover draft admin cart from a prior run.
    env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
        ("state", "=", "draft"),
    ]).sudo().unlink()

    # Also drop any cart that carries a line for our seeded product, in case
    # the prior run logged in as public user.
    tmpl = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if tmpl:
        env["sale.order"].with_context(active_test=False).search([
            ("website_id", "!=", False),
            ("state", "=", "draft"),
            ("order_line.product_template_id", "=", tmpl.id),
        ]).sudo().unlink()
        # Drop stock quants for the product first (required before unlink).
        variants = tmpl.product_variant_ids
        if variants:
            env["stock.quant"].sudo().search(
                [("product_id", "in", variants.ids)]
            ).sudo().unlink()
        tmpl.sudo().unlink()


def setup(env):
    _ensure_website_sale_stock(env)
    _cleanup(env)

    # Locate WH/Stock.
    stock_loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not stock_loc:
        stock_loc = env["stock.location"].search(
            [("usage", "=", "internal"), ("name", "=", "Stock")], limit=1
        )
    if not stock_loc:
        raise RuntimeError("Could not locate WH/Stock location; is stock configured?")

    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": LIST_PRICE,
        "is_published": True,
        "website_published": True,
        # website_sale_stock specific.
        "show_availability": True,
        "available_threshold": AVAILABLE_THRESHOLD,
        "allow_out_of_stock_order": True,
        "taxes_id": [(5, 0, 0)],
    })

    product = tmpl.product_variant_id
    env["stock.quant"]._update_available_quantity(product, stock_loc, STOCK_ON_HAND)

    # Sanity: must have a website to render /shop.
    if not env["website"].search([], limit=1):
        raise RuntimeError("No website record present in DB; cannot run shop test")

    env.cr.execute("SELECT 1")  # flush
