"""Cleanup artifacts from product.configure_stock_route_for_product."""

PRODUCT_NAME = "Bench MTO Item"


def cleanup(env):
    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if not products:
        tmpls = env["product.template"].with_context(active_test=False).search(
            [("name", "=", PRODUCT_NAME)]
        )
        for t in tmpls:
            try:
                t.sudo().unlink()
            except Exception:
                try:
                    t.write({"active": False})
                except Exception:
                    pass
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
        for tmpl in products.mapped("product_tmpl_id"):
            try:
                tmpl.write({"active": False})
            except Exception:
                pass
