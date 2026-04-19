"""Seed for stock.transfer_create_internal_transfer_validate (medium).

Category 5: Deep UI interaction — create-from-scratch stock.picking with a
many2one Operation Type, two many2one locations (one sub-location), one
editable move line, then Mark as Todo + Validate. Pattern distinct from:
  * row 447 (stock.receipt_full_quantity_validate_no_backorder) — pre-made
    incoming receipt, agent only clicks Validate.
  * row 436 (stock.delivery_transfer_validate_partial_backorder_no) —
    pre-made outgoing delivery, agent edits Done cell + handles backorder
    dialog.
  * stock.internal_transfer_between_locations (older) — pre-made internal
    transfer with origin BENCH-INT-SHELF-A1; agent only fills qty +
    validates.

This task forces the agent to:
  1. Open Transfers + click New (no pre-seeded picking).
  2. Pick the Internal Transfers operation type (many2one m2o that updates
     source/destination defaults).
  3. Change the destination from the auto-populated WH/Stock to the
     sub-location WH/Stock/Shelf C.
  4. Add ONE Bench Move Item line with Demand 5.
  5. Mark as Todo then Validate.

Seeds:
  * Storable product `Bench Move Item` (type='consu' + is_storable=True)
    with 10 units on-hand at WH/Stock via
    stock.quant._update_available_quantity.
  * Sub-location `WH/Stock/Shelf C` (usage='internal').
  * Grants admin `stock.group_stock_multi_locations` so the Source /
    Destination Location fields and the Internal Transfers operation type
    are visible.
  * Ensures the WH internal picking type is active (it is by default on
    benchmark_base, but defensive re-enable if ever disabled).
  * Cleans any prior run artifacts (pickings, quants, moves, product).
"""

PRODUCT_NAME = "Bench Move Item"
SHELF_NAME = "Shelf C"
SHELF_COMPLETE = "WH/Stock/Shelf C"
STOCK_COMPLETE = "WH/Stock"
ON_HAND_QTY = 10.0


def _cleanup(env):
    # 1. Destroy any prior internal pickings whose moves touch our product
    #    or whose dest is our shelf. Cancel first so move unlink is safe.
    prod = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("complete_name", "=", SHELF_COMPLETE),
    ], limit=1)

    domain = []
    if prod:
        domain = [("move_ids.product_id", "=", prod.id)]
    if shelf:
        if domain:
            domain = ["|", ("location_dest_id", "=", shelf.id)] + domain
        else:
            domain = [("location_dest_id", "=", shelf.id)]
    if domain:
        pickings = env["stock.picking"].search(domain)
        ordered = sorted(
            pickings, key=lambda p: 0 if p.backorder_id else 1
        )
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

    # 2. Stale moves / quants on the product.
    if prod:
        try:
            env["stock.move.line"].search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            prod.product_tmpl_id.sudo().unlink()
        except Exception:
            pass


def _ensure_stock_location(env):
    loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if not loc:
        wh = env["stock.warehouse"].search([], limit=1)
        loc = wh.lot_stock_id
    return loc


def _ensure_shelf(env, parent_stock):
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("location_id", "=", parent_stock.id),
    ], limit=1)
    if not shelf:
        shelf = env["stock.location"].create({
            "name": SHELF_NAME,
            "location_id": parent_stock.id,
            "usage": "internal",
        })
    return shelf


def setup(env):
    _cleanup(env)

    # Grant admin multi-locations group so Source/Destination fields and
    # the Internal Transfers operation type render on the picking form.
    admin = env.ref("base.user_admin")
    mlg = env.ref(
        "stock.group_stock_multi_locations", raise_if_not_found=False
    )
    if mlg:
        admin.group_ids |= mlg

    # Ensure the warehouse's internal transfer picking type is active.
    wh = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    if wh and wh.int_type_id and not wh.int_type_id.active:
        wh.int_type_id.active = True

    # Ensure WH/Stock and Shelf C exist.
    stock_loc = _ensure_stock_location(env)
    _ensure_shelf(env, stock_loc)

    # Create the storable product.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 25.0,
        "standard_price": 12.0,
        "sale_ok": False,
        "purchase_ok": False,
    })
    product = tmpl.product_variant_id

    # Seed 10 units on-hand at WH/Stock (so reservation on the agent's
    # internal transfer for 5 units succeeds, auto-fills Quantity=5 on
    # Mark as Todo, and Validate goes straight to Done — no backorder).
    env["stock.quant"]._update_available_quantity(
        product, stock_loc, ON_HAND_QTY
    )

    # Flush for determinism.
    env.cr.execute("SELECT 1")
