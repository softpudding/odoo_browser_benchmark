"""Cleanup for mrp.create_bom_kit_type_for_product."""


CLEAN_PRODUCT_NAMES = [
    "Bench Kit Finished",
    "Bench Kit Comp A",
    "Bench Kit Comp B",
]


def cleanup(env):
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", CLEAN_PRODUCT_NAMES),
    ])
    if stale_prod:
        stale_bom = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        try:
            stale_bom.unlink()
        except Exception:
            pass
        try:
            stale_prod.mapped("product_tmpl_id").unlink()
        except Exception:
            pass
