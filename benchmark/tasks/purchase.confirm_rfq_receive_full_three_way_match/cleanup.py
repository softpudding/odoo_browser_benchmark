"""Cleanup artifacts from prior runs of
purchase.confirm_rfq_receive_full_three_way_match."""


VENDOR_NAME = "Bench Supplier Inc"
PRODUCT_A = "Bench 3WM Bracket"
PRODUCT_B = "Bench 3WM Fastener Kit"


def cleanup(env):
    # Any vendor bills for our vendor (shouldn't exist, but safe cleanup).
    bills = env["account.move"].with_context(active_test=False).search([
        ("move_type", "=", "in_invoice"),
        ("partner_id.name", "=", VENDOR_NAME),
    ])
    for b in bills:
        try:
            if b.state == "posted":
                b.button_draft()
            b.button_cancel()
        except Exception:
            pass
        try:
            b.unlink()
        except Exception:
            pass

    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id.name", "=", VENDOR_NAME),
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

    prods = env["product.product"].search([("name", "in", [PRODUCT_A, PRODUCT_B])])
    for p in prods:
        try:
            env["stock.move.line"].search([("product_id", "=", p.id)]).unlink()
            env["stock.move"].search([("product_id", "=", p.id)]).unlink()
            env["product.supplierinfo"].search([
                ("product_tmpl_id", "=", p.product_tmpl_id.id)
            ]).unlink()
        except Exception:
            pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass

    v = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if v:
        other_po = env["purchase.order"].search([("partner_id", "=", v.id)])
        other_bill = env["account.move"].search([("partner_id", "=", v.id)])
        if not other_po and not other_bill:
            try:
                v.unlink()
            except Exception:
                pass
