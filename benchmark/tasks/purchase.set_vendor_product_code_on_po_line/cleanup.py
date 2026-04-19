"""Cleanup for purchase.set_vendor_product_code_on_po_line."""

VENDOR_NAME = "Bench Code Supplier"
PO_NAME = "BENCH-VCODE"
PRODUCT_NAME = "Bench Widget"


def cleanup(env):
    pos = env["purchase.order"].with_context(active_test=False).search([
        "|",
        ("name", "=", PO_NAME),
        ("partner_ref", "=", PO_NAME),
    ])
    for po in pos:
        for bill in po.invoice_ids:
            try:
                if bill.state == "posted":
                    bill.button_draft()
                bill.button_cancel()
                bill.unlink()
            except Exception:
                pass
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

    vendor = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if vendor:
        extra = env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", vendor.id),
        ])
        for po in extra:
            try:
                if po.state in ("purchase", "done"):
                    po.button_cancel()
                po.unlink()
            except Exception:
                pass

    prod = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if prod:
        try:
            env["product.supplierinfo"].search([
                ("product_tmpl_id", "=", prod.product_tmpl_id.id),
            ]).unlink()
        except Exception:
            pass
        try:
            prod.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass

    if vendor:
        try:
            vendor.sudo().unlink()
        except Exception:
            pass
