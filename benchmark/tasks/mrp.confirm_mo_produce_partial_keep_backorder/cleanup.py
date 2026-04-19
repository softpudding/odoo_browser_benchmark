"""Cleanup for mrp.confirm_mo_produce_partial_keep_backorder."""

MO_NAME = "MO-BENCH-PARTIAL"
FINISHED = "Bench Widget"
COMPONENT = "Bench Mat"

PRODUCT_NAMES = [FINISHED, COMPONENT]


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    # Original MO + any backorder siblings (-001, -002, ...).
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
