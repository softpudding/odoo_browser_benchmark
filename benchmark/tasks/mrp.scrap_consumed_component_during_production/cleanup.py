"""Cleanup for mrp.scrap_consumed_component_during_production."""

MO_NAME = "MO-BENCH-SCRAP"
FINISHED = "Bench Assembly Kit"
COMPONENT = "Bench Screw"


def cleanup(env):
    Scrap = env["stock.scrap"]
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    scraps = Scrap.with_context(active_test=False).search([
        ("production_id.name", "=", MO_NAME),
    ])
    for s in scraps:
        if s.state == "draft":
            try:
                s.unlink()
            except Exception:
                pass

    mos = MO.search([("name", "=", MO_NAME)])
    for mo in mos:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    try:
        mos.unlink()
    except Exception:
        pass

    products = Product.with_context(active_test=False).search([
        ("name", "in", [FINISHED, COMPONENT]),
    ])
    boms = BOM.search([
        ("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids),
    ])
    try:
        boms.unlink()
    except Exception:
        pass
    try:
        products.mapped("product_tmpl_id").unlink()
    except Exception:
        pass
