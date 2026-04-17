"""Cleanup for mrp.create_bom_confirm_mo."""


def cleanup(env):
    names = [
        "BenchMaster Assembly Kit",
        "BenchMaster Frame",
        "BenchMaster Panel",
        "BenchMaster Fastener Pack",
    ]
    products = env["product.template"].search([("name", "in", names)])
    variants = products.mapped("product_variant_id")
    env["mrp.production"].search([("product_id", "in", variants.ids)]).unlink()
    env["mrp.bom"].search([("product_tmpl_id", "in", products.ids)]).unlink()
    products.unlink()
