"""Cleanup for mrp.scrap_component_during_partial_production."""

MO_NAME = "M-BENCH-SCRAP-001"
FINISHED = "Bench Widget"
COMP_A = "ScrewA"
COMP_B = "ScrewB"
REASON_TAG = "Defective batch"


def cleanup(env):
    Scrap = env["stock.scrap"]
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    ReasonTag = env["stock.scrap.reason.tag"]

    # Delete any draft scraps linked to the MO; done scraps cannot be
    # unlinked, but they're harmless once we drop the MO/products below.
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

    products = Product.search([("name", "in", [FINISHED, COMP_A, COMP_B])])
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

    # Leave the 'Defective batch' reason tag in place — it may be
    # referenced by done (unremovable) scraps. The next seed reuses it.
    _ = ReasonTag
