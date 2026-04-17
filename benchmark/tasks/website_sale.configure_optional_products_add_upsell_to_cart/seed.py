"""Seed for website_sale.configure_optional_products_add_upsell_to_cart."""


def setup(env):
    env["sale.order"].search([("origin", "=", "website upsell cart")]).unlink()
    env["product.template"].search([
        ("name", "in", ["Docking Console", "Protective Sleeve"]),
    ]).unlink()

    env["product.template"].create({
        "name": "Docking Console",
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 249.0,
        "website_published": True,
    })
    env["product.template"].create({
        "name": "Protective Sleeve",
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 29.0,
        "website_published": False,
    })
