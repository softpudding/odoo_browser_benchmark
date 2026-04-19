"""Cleanup artifacts from stock.create_scrap_order_for_damaged_qty."""

PRODUCT_NAME = "Bench Scrap Item"


def cleanup(env):
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if not prods:
        return

    # Drop draft scrap orders (done ones own immutable stock.move
    # records and cannot be unlinked — leave them).
    try:
        env["stock.scrap"].with_context(active_test=False).search([
            ("product_id", "in", prods.ids),
            ("state", "=", "draft"),
        ]).unlink()
    except Exception:
        pass
    try:
        env["stock.move.line"].search([
            ("product_id", "in", prods.ids),
            ("state", "not in", ("done", "cancel")),
        ]).unlink()
    except Exception:
        pass
    try:
        env["stock.move"].search([
            ("product_id", "in", prods.ids),
            ("state", "not in", ("done", "cancel")),
        ]).unlink()
    except Exception:
        pass
    try:
        env["stock.quant"].with_context(inventory_mode=True).search([
            ("product_id", "in", prods.ids),
        ]).unlink()
    except Exception:
        pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass
