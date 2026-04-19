"""Cleanup for mrp.create_bom_with_components."""


def cleanup(env):
    names = [
        "Bench Assembled Gadget",
        "Bench Steel Frame",
        "Bench Control Board",
        "Bench Power Unit",
    ]
    products = env["product.template"].search([("name", "in", names)])
    variants = products.mapped("product_variant_id")
    if variants:
        env["mrp.production"].search([("product_id", "in", variants.ids)]).unlink()
    if products:
        env["mrp.bom"].search([("product_tmpl_id", "in", products.ids)]).unlink()
        products.unlink()
