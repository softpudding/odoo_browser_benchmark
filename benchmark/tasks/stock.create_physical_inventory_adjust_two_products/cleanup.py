"""Cleanup artifacts from stock.create_physical_inventory_adjust_two_products."""

PRODUCT_X = "Bench Prod X"
PRODUCT_Y = "Bench Prod Y"


def cleanup(env):
    products = env["product.product"].search(
        [("name", "in", [PRODUCT_X, PRODUCT_Y])]
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
