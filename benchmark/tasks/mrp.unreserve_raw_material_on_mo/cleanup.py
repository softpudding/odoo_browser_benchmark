"""Cleanup for mrp.unreserve_raw_material_on_mo."""

MO_NAME = "MO-BENCH-UNRES"
FINISHED = "Bench Unres Product"
COMPONENT = "Bench Unres Mat"

PRODUCT_NAMES = [FINISHED, COMPONENT]


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    mos = MO.search([
        "|",
        ("name", "=", MO_NAME),
        ("name", "=like", MO_NAME + "-%"),
    ])
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
        ("name", "in", PRODUCT_NAMES),
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
