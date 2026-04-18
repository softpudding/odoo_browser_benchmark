"""Seed for stock.transfer_lot_tracked_product.

Category: deep_ui_interaction (HARD).
Creates a lot-tracked product "Lot Product A" and a confirmed incoming
transfer for 50 units. The agent must assign the exact lot number
(LOT-2026-001) and set the done quantity (50) on the move line, then
validate without accepting a backorder.

Differs from stock.receive_lot_tracked_product in that the done quantity
is NOT pre-filled — the agent must enter both lot and quantity.
"""

PRODUCT_NAME = "Lot Product A"
RECEIPT_ORIGIN = "BENCH-TRANSFER-LOT-01"
DEMAND_QTY = 50.0
LOT_NAME = "LOT-2026-001"


def _cleanup(env):
    # Remove any receipts from previous runs
    for pick in env["stock.picking"].search([("origin", "=", RECEIPT_ORIGIN)]):
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.unlink()
        except Exception:
            pass

    # Remove any prior lot records with our target lot name
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        # Remove stock move lines, moves, lots, quants, and the product itself
        env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.quant"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
        prods.mapped("product_tmpl_id").unlink()

    # Also purge any orphan stock.lot rows with our target lot name
    env["stock.lot"].search([("name", "=", LOT_NAME)]).unlink()


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_production_lot")

    # Ensure incoming picking type allows on-the-fly lot creation
    picking_type = env["stock.picking.type"].search(
        [("code", "=", "incoming")], limit=1
    )
    picking_type.write({
        "use_create_lots": True,
        "use_existing_lots": True,
    })

    location_supplier = env.ref("stock.stock_location_suppliers")
    location_stock = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location_stock:
        location_stock = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )

    # Lot-tracked storable product
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "lot",
        "list_price": 75.0,
    })
    product = tmpl.product_variant_id

    # Create the incoming transfer (vendors -> WH/Stock)
    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
        "origin": RECEIPT_ORIGIN,
    })
    env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": DEMAND_QTY,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
    })

    picking.action_confirm()
    picking.action_assign()
    # Do NOT pre-fill the done quantity — the agent must enter it.
