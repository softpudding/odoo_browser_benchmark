"""Cleanup for mrp.unbuild_product_back_to_components."""

FINISHED = "Bench Assembly"
SCREW = "Bench Screw"
HOUSING = "Bench Housing"

PRODUCT_NAMES = [FINISHED, SCREW, HOUSING]


def cleanup(env):
    Unbuild = env["mrp.unbuild"]
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    # 'done' unbuilds cannot be unlinked in a clean way — they leave stock
    # moves behind. Dropping the products below cascades/SQL-cleans what
    # still references them. Draft unbuilds can be unlinked directly.
    stale_unbuild = Unbuild.search([
        ("product_id.name", "=", FINISHED),
    ])
    for u in stale_unbuild:
        if u.state == "draft":
            try:
                u.unlink()
            except Exception:
                pass

    mos = MO.search([
        ("product_id.name", "in", PRODUCT_NAMES),
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
