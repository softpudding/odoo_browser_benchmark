"""Cleanup artifacts from previous runs of the MTO SO->PO task."""


VENDOR_A = "Acme Supply Co"
VENDOR_B = "Brook Trading Ltd"
CUSTOMER_NAME = "Bench MTO Customer"
PRODUCT_NAME = "Bench MTO Widget"
SO_NAME = "S-BENCH-MTO-001"


def cleanup(env):
    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    vendor_a = env["res.partner"].search([("name", "=", VENDOR_A)], limit=1)
    vendor_b = env["res.partner"].search([("name", "=", VENDOR_B)], limit=1)

    # --- SO + chained POs ---
    sos = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)]
    )
    for so in sos:
        linked_pos = env["purchase.order"].with_context(active_test=False).search([
            "|",
            ("origin", "=", so.name),
            ("order_line.sale_line_id.order_id", "=", so.id),
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

        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass
        if so.state in ("sale", "done"):
            try:
                so._action_cancel()
            except Exception:
                pass
        try:
            so.unlink()
        except Exception:
            pass

    # --- Stray POs by vendor (only those that look like ours) ---
    for v in (vendor_a, vendor_b):
        if not v:
            continue
        pos = env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", v.id),
        ])
        for po in pos:
            keep = True
            # Only cleanup POs that reference our SO or vendor product
            if po.origin and SO_NAME in (po.origin or ""):
                keep = False
            elif any(l.product_id.name == PRODUCT_NAME for l in po.order_line):
                keep = False
            if keep:
                continue
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
