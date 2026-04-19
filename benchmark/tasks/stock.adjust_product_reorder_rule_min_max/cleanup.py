"""Cleanup artifacts from stock.adjust_product_reorder_rule_min_max."""

PRODUCT_NAME = "Bench Reorder Item"


def cleanup(env):
    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if not products:
        return

    try:
        env["stock.warehouse.orderpoint"].with_context(
            active_test=False
        ).search([("product_id", "in", products.ids)]).unlink()
    except Exception:
        pass
    try:
        env["stock.move.line"].search(
            [("product_id", "in", products.ids)]
        ).sudo().unlink()
    except Exception:
        pass
    try:
        env["stock.move"].search(
            [("product_id", "in", products.ids)]
        ).sudo().unlink()
    except Exception:
        pass
    try:
        env["stock.quant"].with_context(inventory_mode=True).search(
            [("product_id", "in", products.ids)]
        ).sudo().unlink()
    except Exception:
        pass
    try:
        products.mapped("product_tmpl_id").sudo().unlink()
    except Exception:
        pass
