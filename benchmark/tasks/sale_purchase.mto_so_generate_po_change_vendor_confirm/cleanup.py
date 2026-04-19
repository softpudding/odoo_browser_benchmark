"""Clean up artifacts produced by prior runs of
sale_purchase.mto_so_generate_po_change_vendor_confirm."""


SO_REF = "S-BENCH-MTO-001"
CUSTOMER_NAME = "Harbor MTO Buyer"
PRODUCT_NAME = "Harbor MTO Gadget"
VENDOR_PRIMARY = "Alpha Precision Parts"
VENDOR_ALT = "Orion Component Works"


def cleanup(env):
    # --- 1. SO + linked pickings + linked POs ---
    sos = env["sale.order"].search([("client_order_ref", "=", SO_REF)])
    so_names = sos.mapped("name")

    for order in sos:
        for picking in order.picking_ids:
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass
        linked_pos = env["purchase.order"].search([
            ("origin", "in", list(set(so_names + [SO_REF])) or [SO_REF]),
        ])
        for po in linked_pos:
            for picking in po.picking_ids:
                if picking.state not in ("cancel", "done"):
                    try:
                        picking.action_cancel()
                    except Exception:
                        pass
            if po.state in ("purchase", "done"):
                try:
                    po.button_cancel()
                except Exception:
                    pass
            if po.state == "cancel":
                try:
                    po.button_draft()
                except Exception:
                    pass
            try:
                po.unlink()
            except Exception:
                pass
        if order.state in ("sale", "done"):
            try:
                order._action_cancel()
            except Exception:
                pass
        try:
            order.unlink()
        except Exception:
            pass

    # --- 2. Orphan POs whose origin literally matches the client ref ---
    orphans = env["purchase.order"].search([("origin", "=", SO_REF)])
    for po in orphans:
        if po.state in ("purchase", "done"):
            try:
                po.button_cancel()
            except Exception:
                pass
        try:
            po.unlink()
        except Exception:
            pass

    # --- 3. Product (delete template to remove supplier-info + seller_ids) ---
    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if products:
        env["product.supplierinfo"].search([
            ("product_tmpl_id", "in", products.product_tmpl_id.ids),
        ]).unlink()
        # Any lingering stock moves for this product are cancelled first.
        moves = env["stock.move"].search([("product_id", "in", products.ids)])
        for m in moves.filtered(lambda x: x.state not in ("done", "cancel")):
            try:
                m._action_cancel()
            except Exception:
                pass
        try:
            products.product_tmpl_id.unlink()
        except Exception:
            # Leave it if it's still referenced by done moves.
            pass

    # --- 4. Partners (only if no longer referenced) ---
    for name in (VENDOR_PRIMARY, VENDOR_ALT, CUSTOMER_NAME):
        p = env["res.partner"].search([("name", "=", name)], limit=1)
        if not p:
            continue
        try:
            p.unlink()
        except Exception:
            # Partner may be referenced by residual records; best-effort.
            pass
