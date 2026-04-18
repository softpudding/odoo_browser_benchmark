"""Cleanup for sale_purchase.mto_so_generate_po_change_vendor_confirm."""


SO_REF = "MTO-VENDOR-SWITCH"


def cleanup(env):
    orders = env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", SO_REF),
    ])
    for order in orders:
        linked_pos = env["purchase.order"].with_context(active_test=False).search([
            ("origin", "=", order.name),
        ])
        for po in linked_pos:
            try:
                po.unlink()
            except Exception:
                pass
        try:
            order.unlink()
        except Exception:
            pass
