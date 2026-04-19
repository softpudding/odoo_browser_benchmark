"""Cleanup for mrp_account.mo_consume_and_close_check_valuation."""


MO_NAME = "MO-BENCH-VAL"
FINISHED_NAME = "Bench Assembly"
COMPONENT_NAMES = ["Bench Component 1", "Bench Component 2"]
CATEG_NAME = "Bench Val Real Time"


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Category = env["product.category"]

    stale_mo = MO.search([
        "|",
        ("name", "=", MO_NAME),
        ("name", "=like", MO_NAME + "-%"),
    ])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    stale_mo.unlink()

    clean_names = [FINISHED_NAME] + COMPONENT_NAMES
    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", clean_names),
    ])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    for categ in Category.search([("name", "=", CATEG_NAME)]):
        if not Product.with_context(active_test=False).search_count([
            ("categ_id", "=", categ.id),
        ]):
            try:
                categ.unlink()
            except Exception:
                pass
