"""Remove artifacts created by seed.py."""


def cleanup(env):
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    stale_prod = Product.search([
        ("name", "in", [
            "Benchmark Modular Shelving",
            "Bench Shelf Panel",
            "Bench Shelf Bracket",
            "Bench Shelf Screw",
        ]),
    ])
    if stale_prod:
        BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ]).unlink()
        stale_prod.mapped("product_tmpl_id").unlink()
