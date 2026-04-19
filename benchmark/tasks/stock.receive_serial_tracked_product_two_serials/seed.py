"""Seed for stock.receive_serial_tracked_product_two_serials.

Category 5 (HARD): deep_ui_interaction — Detailed Operations popup + two
serial-number move_line rows on a single serial-tracked move. Classic BU
trap: agent types the first serial into the single pre-reserved move_line
(qty=2 collapsed into one row), Validates, and only one stock.lot gets
created (wrong name often too). Required pattern: open the popup, add a
second row, enter SN-BENCH-A001 / SN-BENCH-A002 one per row with qty=1.

Pre-seeded entities:
  * Vendor 'Bench Serial Vendor' (supplier_rank=1).
  * Storable product 'Bench Serial Item' with tracking='serial'.
  * Receipts picking type: use_create_lots=True AND use_existing_lots=True
    so the Detailed Operations popup exposes the `lot_id` m2o with an
    autocomplete `Create "<text>"` option (both flags are required — one
    alone gives text-only input or hides the Create option).
  * Admin granted `stock.group_production_lot` so the popup renders
    lot_id columns.
  * Incoming picking 'WH/IN/BENCH-SERIAL' for Bench Serial Item qty=2
    from Bench Serial Vendor, action_confirm + action_assign'd so state
    is 'assigned' (Ready). The supplier source location has infinite
    stock, so action_assign auto-creates a single move_line with
    quantity=0 and empty lot_id waiting for the agent's input.

Invariants after setup:
  * picking.state == 'assigned'
  * picking.move_ids has exactly 1 move, product_uom_qty == 2.0
  * No stock.lot named SN-BENCH-A001 / SN-BENCH-A002 exists yet.
"""

PICKING_NAME = "WH/IN/BENCH-SERIAL"
VENDOR_NAME = "Bench Serial Vendor"
PRODUCT_NAME = "Bench Serial Item"
DEMAND_QTY = 2.0
EXPECTED_SERIALS = ("SN-BENCH-A001", "SN-BENCH-A002")


def _cleanup(env):
    # Pickings matching our pinned name or any incoming picking for our
    # vendor. Include cancelled / done leftovers from prior aborted runs.
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

    # Stale move_lines / moves / quants / lots for the product.
    prods = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
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
            quants = env["stock.quant"].search(
                [("product_id", "in", prods.ids)]
            )
            for q in quants:
                try:
                    q.with_context(inventory_mode=True).write(
                        {"inventory_quantity": 0.0}
                    )
                    q.action_apply_inventory()
                except Exception:
                    pass
            try:
                quants.unlink()
            except Exception:
                pass
        except Exception:
            pass
        try:
            env["stock.lot"].search(
                [("product_id", "in", prods.ids)]
            ).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    # Also clear any orphan lots that match the expected serial names
    # (from a prior failed run that created them under a deleted product).
    stale_lots = env["stock.lot"].search(
        [("name", "in", list(EXPECTED_SERIALS))]
    )
    if stale_lots:
        try:
            stale_lots.unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    # Grant admin the lot/serial-tracking group so the Detailed Operations
    # popup exposes the lot_id m2o column (without it, the popup only
    # shows quantity).
    admin = env.ref("base.user_admin")
    grp = env.ref("stock.group_production_lot", raise_if_not_found=False)
    if grp and admin not in grp.user_ids:
        grp.sudo().write({"user_ids": [(4, admin.id)]})

    # Receipts picking type: allow BOTH create + existing so the popup's
    # lot_id autocomplete shows the Create "<text>" option (requires
    # use_existing_lots=True) AND will accept new names typed on the fly
    # (requires use_create_lots=True).
    picking_type = env["stock.picking.type"].search(
        [("code", "=", "incoming")], limit=1
    )
    picking_type.write({
        "use_create_lots": True,
        "use_existing_lots": True,
    })

    # Vendor.
    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "orders@benchserialvendor.example",
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # Storable serial-tracked product.
    product_tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "serial",
        "list_price": 400.0,
        "standard_price": 220.0,
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

    # Incoming picking type scoped to this warehouse, so the picking lands
    # under WH/IN.
    in_type = wh.in_type_id

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
    # For incoming moves the source is the supplier location (infinite
    # availability), so action_assign() succeeds immediately. For a
    # serial-tracked move with demand=2 and use_create_lots/use_existing
    # BOTH True, Odoo 19's _action_assign creates a SINGLE move_line
    # with quantity=0.0 (no auto-fill, since serial lots are unknown
    # until the agent enters them). The Details popup is then the only
    # place to enter the two serials.
    picking.action_assign()

    # Ensure state is 'assigned' (Ready). Belt-and-suspenders.
    if picking.state != "assigned":
        try:
            picking.move_ids._action_assign()
        except Exception:
            pass

    # Invariants.
    if picking.state != "assigned":
        raise RuntimeError(
            f"Seed invariant failed: picking.state={picking.state!r}, "
            f"expected 'assigned' (Ready)"
        )
    moves = picking.move_ids
    if len(moves) != 1:
        raise RuntimeError(
            f"Seed invariant failed: expected exactly 1 move, got "
            f"{len(moves)}"
        )
    if abs(moves[0].product_uom_qty - DEMAND_QTY) > 1e-6:
        raise RuntimeError(
            f"Seed invariant failed: move demand is "
            f"{moves[0].product_uom_qty!r}, expected {DEMAND_QTY}"
        )
    if moves[0].product_id.tracking != "serial":
        raise RuntimeError(
            f"Seed invariant failed: product tracking is "
            f"{moves[0].product_id.tracking!r}, expected 'serial'"
        )
    stale = env["stock.lot"].search(
        [("name", "in", list(EXPECTED_SERIALS))]
    )
    if stale:
        raise RuntimeError(
            f"Seed invariant failed: stale serial lots still exist: "
            f"{stale.mapped('name')}"
        )
