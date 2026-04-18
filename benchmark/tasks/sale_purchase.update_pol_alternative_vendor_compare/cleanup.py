"""Cleanup artifacts from previous runs of the alternative-RFQ task."""


VENDOR_NAMES = ["Atlas Industrial", "Beacon Mechanical", "Crestline Equipment"]
RFQ_REF = "R-BENCH-ALT-001"


def cleanup(env):
    pos = env["purchase.order"].with_context(active_test=False).search([
        ("origin", "=", RFQ_REF),
    ])
    for name in VENDOR_NAMES:
        v = env["res.partner"].search([("name", "=", name)], limit=1)
        if v:
            pos |= env["purchase.order"].with_context(active_test=False).search([
                ("partner_id", "=", v.id),
            ])

    for po in pos:
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
            try:
                po.purchase_group_id = False
                po.unlink()
            except Exception:
                pass

    for g in env["purchase.order.group"].search([]):
        if not g.order_ids:
            try:
                g.unlink()
            except Exception:
                pass
