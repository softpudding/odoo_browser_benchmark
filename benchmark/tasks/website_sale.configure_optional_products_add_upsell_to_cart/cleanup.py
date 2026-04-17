"""Cleanup for website_sale.configure_optional_products_add_upsell_to_cart."""


def cleanup(env):
    env["sale.order"].search([("origin", "=", "website upsell cart")]).unlink()
    env["product.template"].search([
        ("name", "in", ["Docking Console", "Protective Sleeve"]),
    ]).unlink()
