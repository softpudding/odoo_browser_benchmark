"""Seed a validated delivery from a confirmed+invoiced SO for the return+credit-note task.

Category 3 (HARD): The agent must open a done delivery, create a partial
return via the Return wizard (editing quantities), validate the return,
navigate to the sales order, find the posted invoice, create a credit note
with specific reason and date, then confirm. Crosses Stock -> Sales ->
Accounting modules.
"""

from datetime import date


def setup(env):
    # ------------------------------------------------------------------
    # Partners
    # ------------------------------------------------------------------
    partner = env["res.partner"].search(
        [("name", "=", "Cascade Dynamics")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Cascade Dynamics",
            "email": "orders@cascadedynamics.com",
            "customer_rank": 1,
        })
    else:
        partner.write({"customer_rank": max(partner.customer_rank, 1)})

    distractor_partner = env["res.partner"].search(
        [("name", "=", "Cascade Design")], limit=1
    )
    if not distractor_partner:
        distractor_partner = env["res.partner"].create({
            "name": "Cascade Design",
            "email": "info@cascadedesign.com",
            "customer_rank": 1,
        })

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------
    products = {}
    for name, price in [("Industrial Fan Unit", 180.0), ("Rubber Gasket Set", 45.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price * 0.6,
                "invoice_policy": "order",
                "sale_ok": True,
            })
            p = tmpl.product_variant_id
        else:
            p.product_tmpl_id.write({
                "type": "consu",
                "list_price": price,
                "invoice_policy": "order",
                "sale_ok": True,
            })
        p.is_storable = True
        products[name] = p

    # ------------------------------------------------------------------
    # Ensure stock for delivery
    # ------------------------------------------------------------------
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    for name, qty in [("Industrial Fan Unit", 200), ("Rubber Gasket Set", 200)]:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": products[name].id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    # ------------------------------------------------------------------
    # Cleanup prior runs
    # ------------------------------------------------------------------
    # Remove credit notes / invoices linked to our SO
    old_sos = env["sale.order"].search([
        ("client_order_ref", "in", ["BENCH-DEL-RET", "BENCH-DEL-RET-DIST"]),
    ])
    for so in old_sos:
        for inv in so.invoice_ids:
            if inv.state == "posted":
                inv.button_draft()
            inv.button_cancel()
            inv.unlink()

    # Remove return pickings first (they reference original pickings)
    for so in old_sos:
        for picking in so.picking_ids:
            # Find return pickings that reference this one
            returns = env["stock.picking"].search([
                ("return_id", "=", picking.id),
            ])
            for ret in returns:
                if ret.state not in ("cancel", "done"):
                    ret.action_cancel()
                ret.move_ids.write({"state": "cancel"})
                ret.write({"state": "cancel"})
                ret.unlink()

    # Now remove original pickings
    for so in old_sos:
        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
            picking.move_ids.write({"state": "cancel"})
            picking.write({"state": "cancel"})
            picking.unlink()

    # Remove old SOs
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

    # ------------------------------------------------------------------
    # Create and confirm Sales Order
    # ------------------------------------------------------------------
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "BENCH-DEL-RET",
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Industrial Fan Unit"].id,
        "product_uom_qty": 10,
        "price_unit": 180.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Rubber Gasket Set"].id,
        "product_uom_qty": 20,
        "price_unit": 45.0,
        "tax_ids": [(5, 0, 0)],
    })
    so.action_confirm()

    # ------------------------------------------------------------------
    # Fully deliver (validate the picking)
    # ------------------------------------------------------------------
    picking = so.picking_ids[0]
    for move in picking.move_ids:
        move.quantity = move.product_uom_qty
    picking.button_validate()

    # Rename picking origin for easy identification
    picking.write({"origin": "BENCH-DEL-RET"})

    # ------------------------------------------------------------------
    # Create and post invoice
    # ------------------------------------------------------------------
    invoice = so._create_invoices()
    invoice.write({"invoice_date": date(2026, 5, 15)})
    invoice.action_post()

    # ------------------------------------------------------------------
    # Distractor: another delivery for "Cascade Design" (similar name)
    # ------------------------------------------------------------------
    dist_so = env["sale.order"].create({
        "partner_id": distractor_partner.id,
        "client_order_ref": "BENCH-DEL-RET-DIST",
    })
    env["sale.order.line"].create({
        "order_id": dist_so.id,
        "product_id": products["Industrial Fan Unit"].id,
        "product_uom_qty": 5,
        "price_unit": 180.0,
        "tax_ids": [(5, 0, 0)],
    })
    dist_so.action_confirm()

    dist_picking = dist_so.picking_ids[0]
    for move in dist_picking.move_ids:
        move.quantity = move.product_uom_qty
    dist_picking.button_validate()
    dist_picking.write({"origin": "BENCH-DEL-RET-DIST"})
