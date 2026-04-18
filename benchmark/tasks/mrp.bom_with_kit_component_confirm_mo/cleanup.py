"""Cleanup for mrp.bom_with_kit_component_confirm_mo."""


MO_NAME = "M-BENCH-KIT-001"
CLEAN_PRODUCT_NAMES = [
    "Bench Assembly",
    "Bench Kit",
    "Bench Frame",
    "Bench Sub-A",
    "Bench Sub-B",
]


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

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

    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", CLEAN_PRODUCT_NAMES),
    ])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()
