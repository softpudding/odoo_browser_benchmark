"""Cleanup artifacts from prior runs of
purchase.create_rfq_receive_invoice_3way_match."""


VENDOR_NAME = "Bench Supply Co"
DISTRACTOR_VENDOR = "Bench Filler Vendor"
PRODUCT_A = "Bench PO Item A"
PRODUCT_B = "Bench PO Item B"
BILL_REF = "BSC-BILL-3WM"


def cleanup(env):
    # Drop any draft / posted bills the agent produced.
    bills = env["account.move"].with_context(active_test=False).search([
        "|",
        ("ref", "=", BILL_REF),
        "&",
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

    # POs for our vendor + distractor vendor.
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("partner_id.name", "in", [VENDOR_NAME, DISTRACTOR_VENDOR]),
    ])
    for po in pos:
        for b in po.invoice_ids:
            try:
                if b.state == "posted":
                    b.button_draft()
                b.button_cancel()
                b.unlink()
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

    # Products — try to unlink the templates.
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

    # Vendors (only if nothing still references them).
    for vname in (VENDOR_NAME, DISTRACTOR_VENDOR):
        v = env["res.partner"].search([("name", "=", vname)], limit=1)
        if not v:
            continue
        other_po = env["purchase.order"].search([("partner_id", "=", v.id)])
        other_bill = env["account.move"].search([("partner_id", "=", v.id)])
        if not other_po and not other_bill:
            try:
                v.unlink()
            except Exception:
                pass
