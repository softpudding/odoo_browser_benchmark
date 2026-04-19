"""Seed for stock.receipt_full_quantity_validate_no_backorder.

Category 1 (EASY): deep_ui_interaction — single-click Validate on a Ready
incoming receipt whose Quantity (Done) already matches Demand exactly, so
no Create Backorder dialog appears. Easy calibration anchor.

Seeds:
  * Vendor 'Bench Vendor'.
  * Storable product 'Bench Recv Item' (type='consu', is_storable=True,
    tracking='none').
  * A Ready (reserved / assigned) incoming receipt picking
    'WH/IN/BENCH-FULL' for 10 units of Bench Recv Item from the vendor.
    The picking is action_confirm + action_assign'd so its state is
    'assigned' and the single move.quantity == product_uom_qty == 10
    (Done auto-fills on an incoming move when the picking is assigned —
    no reservation is needed because the source is the supplier location).

The agent must:
  1. Open the Inventory Receipts list.
  2. Open the receipt WH/IN/BENCH-FULL.
  3. Click Validate in the header.

Because qty_done matches demand exactly, NO Create Backorder? dialog
appears. The picking flips straight to state='done' and a
stock.quant at WH/Stock lands for Bench Recv Item quantity=10.
"""

PICKING_NAME = "WH/IN/BENCH-FULL"
VENDOR_NAME = "Bench Vendor"
PRODUCT_NAME = "Bench Recv Item"
DEMAND_QTY = 10.0


def _cleanup(env):
    # Remove old pickings referencing our pinned name / vendor.
    pickings = env["stock.picking"].search([
        "|",
        ("name", "=", PICKING_NAME),
        "&",
        ("partner_id.name", "=", VENDOR_NAME),
        ("picking_type_id.code", "=", "incoming"),
    ])
    # Cancel backorders first (children), then originals.
    ordered = sorted(pickings, key=lambda p: 0 if p.backorder_id else 1)
    for pick in ordered:
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
            pick.write({"state": "cancel"})
        except Exception:
            pass
        try:
            pick.unlink()
        except Exception:
            pass

    # Stale quants + moves / move lines on the product.
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        try:
            env["stock.move.line"].search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    # Vendor.
    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "ops@benchvendor.example",
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # Storable product so the stock.quant lands at WH/Stock after validate.
    product_tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 20.0,
        "standard_price": 10.0,
        "sale_ok": False,
        "purchase_ok": True,
    })
    product = product_tmpl.product_variant_id

    # Locations.
    wh = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    stock_location = wh.lot_stock_id
    supplier_location = env.ref("stock.stock_location_suppliers")

    # Incoming picking type for this warehouse.
    in_type = wh.in_type_id

    # Create the picking with a pinned name so we can find it
    # deterministically and so backorder-checking entity_keys resolve to
    # that same display_name if a (bug-path) backorder were ever made.
    picking = env["stock.picking"].create({
        "picking_type_id": in_type.id,
        "partner_id": vendor.id,
        "location_id": supplier_location.id,
        "location_dest_id": stock_location.id,
        "origin": PICKING_NAME,
        "name": PICKING_NAME,
    })
    env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": DEMAND_QTY,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": supplier_location.id,
        "location_dest_id": stock_location.id,
    })

    picking.action_confirm()
    # For an incoming move the source is the supplier location (infinite
    # availability), so action_assign succeeds immediately and auto-fills
    # move.quantity = product_uom_qty (10) on the single move_line. That
    # means clicking Validate will NOT trigger the Create Backorder?
    # dialog — the picking jumps straight to 'done'.
    picking.action_assign()

    # Belt-and-suspenders: make sure quantity is pre-filled so the agent
    # has zero cells to edit. If for some reason action_assign didn't
    # auto-fill (edge cases observed on some benchmark_base snapshots),
    # force-write the move.quantity so the agent sees 10.00 in Done.
    for mv in picking.move_ids:
        if (mv.quantity or 0.0) < DEMAND_QTY - 1e-6:
            mv.quantity = DEMAND_QTY
    # Also pre-flag picked so button_validate does not raise an
    # availability wizard on empty picked flag (Odoo 19 behavior).
    try:
        picking.move_ids.write({"picked": True})
    except Exception:
        pass

    # Ensure state is 'assigned' (Ready).
    if picking.state != "assigned":
        try:
            picking.move_ids._action_assign()
        except Exception:
            pass
