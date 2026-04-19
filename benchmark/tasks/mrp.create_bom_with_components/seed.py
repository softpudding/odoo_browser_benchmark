"""Seed products for mrp.create_bom_with_components.

Creates 4 storable products (1 finished good + 3 components) and
cleans up any pre-existing BoMs/products from prior runs so the task
always starts from a clean slate.
"""

PRODUCT_NAME = "Bench Assembled Gadget"
COMPONENTS = [
    ("Bench Steel Frame", 1.0),
    ("Bench Control Board", 1.0),
    ("Bench Power Unit", 2.0),
]


def setup(env):
    cleanup_names = [PRODUCT_NAME, *[name for name, _qty in COMPONENTS]]

    products = env["product.template"].search([("name", "in", cleanup_names)])
    variants = products.mapped("product_variant_id")
    if variants:
        env["mrp.production"].search([("product_id", "in", variants.ids)]).unlink()
    if products:
        env["mrp.bom"].search([("product_tmpl_id", "in", products.ids)]).unlink()
        products.unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "is_storable": True,
        "sale_ok": True,
        "purchase_ok": False,
    })

    for component_name, _qty in COMPONENTS:
        env["product.template"].create({
            "name": component_name,
            "is_storable": True,
            "sale_ok": False,
            "purchase_ok": True,
        })
