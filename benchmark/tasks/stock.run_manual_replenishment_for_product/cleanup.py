"""Cleanup artifacts from stock.run_manual_replenishment_for_product."""

VENDOR_NAME = "Bench Replenish Vendor"
PRODUCT_NAME = "Bench Replenish Item"


def cleanup(env):
    vendor = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if vendor:
        pos = env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", vendor.id),
        ])
        for po in pos:
            for p in po.picking_ids:
                if p.state not in ("done", "cancel"):
                    try:
                        p.action_cancel()
                    except Exception:
                        pass
                try:
                    p.move_ids.write({"state": "cancel"})
                    p.write({"state": "cancel"})
                    p.unlink()
                except Exception:
                    pass
            try:
                if po.state in ("purchase", "done"):
                    po.button_cancel()
                po.unlink()
            except Exception:
                pass

    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if products:
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
            env["product.supplierinfo"].search(
                [("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids)]
            ).unlink()
        except Exception:
            pass
        try:
            products.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass

    if vendor:
        try:
            other_po = env["purchase.order"].search([
                ("partner_id", "=", vendor.id),
            ])
            other_bill = env["account.move"].search([
                ("partner_id", "=", vendor.id),
            ])
            if not other_po and not other_bill:
                vendor.unlink()
        except Exception:
            pass
