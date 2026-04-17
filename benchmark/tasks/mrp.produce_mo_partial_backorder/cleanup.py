"""Clean up artifacts from previous runs of mrp.produce_mo_partial_backorder."""


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    stale_mo = MO.search([
        "|",
        ("name", "=", "WH/MO/BENCH-PART-001"),
        ("name", "=like", "WH/MO/BENCH-PART-001-%"),
    ])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    stale_mo.unlink()

    stale_prod = Product.search([
        ("name", "in", [
            "Bench Chassis Z",
            "Bench Frame Panel",
            "Bench Bolt Pack",
        ]),
    ])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()
