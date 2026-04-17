"""Seed for stock.receive_lot_tracked_product.

Category: deep_ui_interaction (HARD).
Creates a lot-tracked product and a confirmed receipt for 20 units.
The agent must assign the exact lot number (LOT-2026-R042) on the move
line and validate — without a lot, Odoo blocks validation.
"""

PRODUCT_NAME = "Apex Turbine Rotor"
RECEIPT_ORIGIN = "BENCH-LOT-RCV-01"
DEMAND_QTY = 20.0


def _cleanup(env):
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

    # Delete prior runs' products (and any move lines still referencing them).
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
    env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
    prods.mapped("product_tmpl_id").unlink()


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_production_lot")

    # Ensure the Receipts picking type allows on-the-fly lot creation.
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

    # Lot-tracked storable product.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "lot",
        "list_price": 1200.0,
    })
    product = tmpl.product_variant_id

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

    # Pre-populate the done quantity so the task is purely about
    # entering the lot and validating. Without this, the agent would
    # also have to fill the Quantity column.
    for ml in picking.move_line_ids:
        ml.quantity = DEMAND_QTY
