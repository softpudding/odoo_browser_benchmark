"""Seed for stock.receive_serial_tracked_product.

Category: deep_ui_interaction (HARD).

Creates a draft incoming stock.picking with origin BENCH-SN-RCV-01
containing a single move for 3 units of the serial-tracked product
'Bench Serial Gadget'. The agent must split the move into three
move-lines of quantity 1 and assign the exact serial numbers
SN-BENCH-001 / SN-BENCH-002 / SN-BENCH-003 in the Detailed Operations
popup, then Validate the receipt.

Source location: Partners/Vendors (stock.stock_location_suppliers).
Destination:     WH/Stock.

The seed leaves the picking in a confirmable state (draft). The prompt
instructs the agent to Mark as Todo / Confirm before entering details.
The picking type has use_create_lots=True so serials can be created
on the fly from the popup.
"""

PRODUCT_NAME = "Bench Serial Gadget"
RECEIPT_ORIGIN = "BENCH-SN-RCV-01"
DEMAND_QTY = 3.0
SERIAL_NAMES = ("SN-BENCH-001", "SN-BENCH-002", "SN-BENCH-003")


def _cleanup(env):
    # Any picking we previously seeded (by origin).
    for pick in env["stock.picking"].search([("origin", "=", RECEIPT_ORIGIN)]):
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.move_ids.write({"state": "cancel"})
        except Exception:
            pass
        try:
            pick.unlink()
        except Exception:
            pass

    # Delete leftover product + cascading stock records for idempotency.
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.quant"].search([("product_id", "in", prods.ids)]).unlink()
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    # Also drop any stray lots whose name matches the expected serials.
    stale_lots = env["stock.lot"].search([("name", "in", list(SERIAL_NAMES))])
    if stale_lots:
        try:
            stale_lots.unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    # Enable lots/serials UI feature for admin.
    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_production_lot")

    # Make sure the incoming Receipts picking type lets the agent create
    # lots/serials on the fly from the operations popup.
    picking_type = env["stock.picking.type"].search(
        [("code", "=", "incoming")], limit=1
    )
    if not picking_type:
        raise RuntimeError("No incoming picking type found on the warehouse")
    picking_type.write({
        "use_create_lots": True,
        "use_existing_lots": True,
    })

    # Serial-tracked storable product.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "serial",
        "list_price": 450.0,
        "standard_price": 200.0,
    })
    product = tmpl.product_variant_id

    # Locations.
    location_supplier = env.ref("stock.stock_location_suppliers")
    location_stock = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location_stock:
        location_stock = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    if not location_stock:
        raise RuntimeError("Could not find WH/Stock destination location")

    # Draft incoming picking.
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

    # Leave the picking in DRAFT. The prompt asks the agent to confirm.
    # (The oracle will call action_confirm/action_assign via JSON-RPC.)

    # Sanity checks.
    assert picking.state == "draft", (
        f"Seed failed: picking should be draft, got {picking.state}"
    )
    assert len(picking.move_ids) == 1, (
        f"Seed failed: expected exactly 1 move, got {len(picking.move_ids)}"
    )
    assert picking.move_ids[0].product_id == product, (
        "Seed failed: move is not on the Bench Serial Gadget product"
    )
    assert picking.move_ids[0].product_uom_qty == DEMAND_QTY, (
        f"Seed failed: move demand should be {DEMAND_QTY}, "
        f"got {picking.move_ids[0].product_uom_qty}"
    )
    assert product.tracking == "serial", (
        "Seed failed: Bench Serial Gadget must be tracking='serial'"
    )

    env.cr.execute("SELECT 1")  # force flush
