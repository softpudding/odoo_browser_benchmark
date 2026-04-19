"""Cleanup artifacts from stock.adjust_inventory_count_apply_moves."""

PRODUCT_A = "Bench Prod A"
PRODUCT_B = "Bench Prod B"


def cleanup(env):
    products = env["product.product"].search(
        [("name", "in", [PRODUCT_A, PRODUCT_B])]
    )
    if products:
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
