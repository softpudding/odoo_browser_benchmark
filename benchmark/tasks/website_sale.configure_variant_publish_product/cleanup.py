"""Cleanup for website_sale.configure_variant_publish_product."""


def cleanup(env):
    product = env["product.template"].search([("name", "=", "Field Pack Duffel")], limit=1)
    if product:
        product.write({
            "website_published": False,
            "attribute_line_ids": [(5, 0, 0)],
        })
