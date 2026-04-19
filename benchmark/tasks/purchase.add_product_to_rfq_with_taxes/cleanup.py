"""Cleanup for purchase.add_product_to_rfq_with_taxes."""

VENDOR_NAME = "Bench Tax Vendor"
PO_NAME = "BENCH-ADD-TAX"
PRODUCT_EXISTING = "Bench Other Item"
PRODUCT_NEW = "Bench Taxable Item"
TAX_NAME = "Bench Tax 5%"


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

    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "in", [PRODUCT_EXISTING, PRODUCT_NEW])]
    )
    if prods:
        try:
            env["product.supplierinfo"].search([
                ("product_tmpl_id", "in", prods.mapped("product_tmpl_id").ids),
            ]).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass

    taxes = env["account.tax"].with_context(active_test=False).search([
        ("name", "=", TAX_NAME),
    ])
    for t in taxes:
        try:
            t.sudo().unlink()
        except Exception:
            pass

    if vendor:
        try:
            vendor.sudo().unlink()
        except Exception:
            pass
