"""Seed a validated receipt for stock.scrap_product_from_receipt.

Creates a done incoming stock.picking (receipt) BENCH-RCV-SCRAP-01 for
the product "Bench Scrap Product" with 10 units received into WH/Stock.
The agent must open this receipt and scrap 2 units via the Scrap action.
"""

PRODUCT_NAME = "Bench Scrap Product"
RECEIPT_REF = "BENCH-RCV-SCRAP-01"


def setup(env):
    # --- Cleanup prior runs (scraps first, then pickings, then product) ---
    env["stock.scrap"].search([
        ("product_id.display_name", "=", PRODUCT_NAME),
    ]).sudo().unlink()

    old_picks = env["stock.picking"].search([("origin", "=", RECEIPT_REF)])
    for pick in old_picks:
        try:
            if pick.state != "done":
                pick.action_cancel()
            pick.unlink()
        except Exception:
            # Done pickings can't be deleted by normal users; try sudo/force
            try:
                pick.sudo().unlink()
            except Exception:
                pass

    # Also clean stray moves/lines referencing the product just in case
    env["stock.move.line"].search([
        ("product_id.display_name", "=", PRODUCT_NAME),
        ("state", "!=", "done"),
    ]).unlink()

    # Clean up product if leftover from earlier runs
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    # --- Ensure locations & picking type ---
    location_supplier = env.ref("stock.stock_location_suppliers")
    location_stock = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location_stock:
        location_stock = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )

    picking_type = env["stock.picking.type"].search(
        [("code", "=", "incoming")], limit=1
    )

    # --- Create the product (storable, so we have on-hand qty to scrap) ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "list_price": 15.0,
    })
    product = tmpl.product_variant_id

    # --- Create the receipt and fully receive 10 units ---
    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
        "origin": RECEIPT_REF,
    })

    env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": 10.0,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
    })

    picking.action_confirm()
    picking.action_assign()

    # Set done quantity on each move line and validate
    for move in picking.move_ids:
        move.quantity = move.product_uom_qty
        move.picked = True

    picking.button_validate()
    # If any wizard appears (e.g. immediate transfer), try to process it
    # button_validate on a fully-picked receipt should complete directly.
    assert picking.state == "done", (
        f"Seed failed: expected receipt state 'done', got '{picking.state}'"
    )
