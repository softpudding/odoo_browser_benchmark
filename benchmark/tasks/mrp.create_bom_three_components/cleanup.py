"""Cleanup for mrp.create_bom_three_components."""


def cleanup(env):
    names = [
        "Wooden Chair",
        "Wooden Leg",
        "Seat Board",
        "Backrest Panel",
    ]
    products = env["product.template"].search([("name", "in", names)])
    variants = products.mapped("product_variant_id")
    env["mrp.production"].search([("product_id", "in", variants.ids)]).unlink()
    env["mrp.bom"].search([("product_tmpl_id", "in", products.ids)]).unlink()
    products.unlink()
