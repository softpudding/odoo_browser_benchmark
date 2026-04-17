"""Seed products for the manufacturing BOM creation task."""

from odoo.fields import Command


PRODUCT_NAME = "BenchMaster Assembly Kit"
COMPONENTS = [
    ("BenchMaster Frame", 2.0),
    ("BenchMaster Panel", 4.0),
    ("BenchMaster Fastener Pack", 1.0),
]


def setup(env):
    cleanup_products = [PRODUCT_NAME, *[name for name, _qty in COMPONENTS]]

    products = env["product.template"].search([("name", "in", cleanup_products)])
    variants = products.mapped("product_variant_id")
    env["mrp.production"].search([("product_id", "in", variants.ids)]).unlink()
    env["mrp.bom"].search([("product_tmpl_id", "in", products.ids)]).unlink()
    products.unlink()

    finished = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
    })

    for component_name, _qty in COMPONENTS:
        env["product.template"].create({
            "name": component_name,
            "type": "consu",
            "sale_ok": False,
            "purchase_ok": True,
        })

