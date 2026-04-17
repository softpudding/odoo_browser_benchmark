"""Cleanup for mrp.surgical_bom_component_qty_edit."""

NAMES = [
    "Benchmark Assembly Gamma",
    "Gamma Frame",
    "Gamma Panel",
    "Gamma Bolt M6",
    "Gamma Cable",
    "Gamma Sticker",
]


def cleanup(env):
    prods = env["product.product"].search([("name", "in", NAMES)])
    boms = env["mrp.bom"].search([
        ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
    ])
    boms.unlink()
    prods.mapped("product_tmpl_id").unlink()
