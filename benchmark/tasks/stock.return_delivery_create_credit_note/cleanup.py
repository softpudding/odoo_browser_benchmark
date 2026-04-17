"""Clean up artifacts from previous runs."""


def cleanup(env):
    # Find all SOs created by our seed
    old_sos = env["sale.order"].search([
        ("client_order_ref", "in", ["BENCH-DEL-RET", "BENCH-DEL-RET-DIST"]),
    ])

    # Remove invoices / credit notes
    for so in old_sos:
        for inv in so.invoice_ids:
            if inv.state == "posted":
                inv.button_draft()
            inv.button_cancel()
            inv.unlink()

    # Remove return pickings first
    for so in old_sos:
        for picking in so.picking_ids:
            returns = env["stock.picking"].search([
                ("return_id", "=", picking.id),
            ])
            for ret in returns:
                if ret.state not in ("cancel", "done"):
                    ret.action_cancel()
                ret.move_ids.write({"state": "cancel"})
                ret.write({"state": "cancel"})
                ret.unlink()

    # Remove original pickings
    for so in old_sos:
        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
            picking.move_ids.write({"state": "cancel"})
            picking.write({"state": "cancel"})
            picking.unlink()

    # Remove SOs
    for so in old_sos:
        if so.state in ("sale", "done"):
            so.with_context(disable_cancel_warning=True)._action_cancel()
        so.unlink()

    # Also clean standalone pickings with our origin
    for origin in ("BENCH-DEL-RET", "BENCH-DEL-RET-DIST"):
        old_picks = env["stock.picking"].search([("origin", "=", origin)])
        for pk in old_picks:
            returns = env["stock.picking"].search([("return_id", "=", pk.id)])
            for ret in returns:
                if ret.state not in ("cancel", "done"):
                    ret.action_cancel()
                ret.move_ids.write({"state": "cancel"})
                ret.write({"state": "cancel"})
                ret.unlink()
            if pk.state not in ("cancel", "done"):
                pk.action_cancel()
            pk.move_ids.write({"state": "cancel"})
            pk.write({"state": "cancel"})
            pk.unlink()

    # Clean up partners if no other references
    for name in ("Cascade Dynamics", "Cascade Design"):
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        if partner:
            remaining_sos = env["sale.order"].search([
                ("partner_id", "=", partner.id),
            ])
            if not remaining_sos:
                partner.unlink()
