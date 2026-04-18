"""Seed for purchase_stock.receive_partial_scrap_damaged_units.

Category 3 (HARD): side_effect_trap — partial receive + scrap wizard +
backorder dialog combine three known browser-use pain points.

Seeds:
  * Vendor 'Bench Parts Vendor'
  * Consumable product 'Bench Parts' (type='consu', is_storable=False)
    so the scrap wizard skips the Insufficient-Quantity check.
  * A custom inventory-type location 'Lost' under the main warehouse
    (complete_name = 'WH/Lost'), flagged as a scrap destination by
    having usage='inventory'.
  * A confirmed purchase.order 'P-BENCH-DMG-001' for 20 units of
    Bench Parts, whose auto-generated receipt is already assigned
    (Ready) and waiting for the agent.

The agent must:
  1. Open the PO, click Receipt smart button.
  2. Change Done qty on the move line from the default 20 to 15.
  3. Open cog Actions menu > Scrap, fill the dialog with
     product=Bench Parts, scrap_qty=5 (NOT the default 1),
     scrap_location_id=WH/Lost (NOT the default Scrap location),
     then click Scrap Products.
  4. On the picking, click Validate and choose **Create Backorder**
     in the confirmation dialog.
"""

PO_ORIGIN = "P-BENCH-DMG-001"
VENDOR_NAME = "Bench Parts Vendor"
PRODUCT_NAME = "Bench Parts"
LOST_LOCATION_NAME = "Lost"
DEMAND_QTY = 20.0


def _cleanup(env):
    # Remove any stale scrap records tied to our product.
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        scraps = env["stock.scrap"].with_context(active_test=False).search([
            ("product_id", "in", prods.ids),
        ])
        for s in scraps:
            try:
                if s.state == "draft":
                    s.unlink()
            except Exception:
                pass

    # Cancel + unlink old pickings for this vendor / origin.
    pickings = env["stock.picking"].search([
        "|",
        ("origin", "=", PO_ORIGIN),
        "&",
        ("partner_id.name", "=", VENDOR_NAME),
        ("picking_type_id.code", "=", "incoming"),
    ])
    for pick in pickings:
        if pick.state not in ("done", "cancel"):
            try:
                pick.action_cancel()
            except Exception:
                pass
        try:
            pick.move_ids.write({"state": "cancel"})
            pick.write({"state": "cancel"})
            pick.unlink()
        except Exception:
            pass

    # Old POs for same vendor / origin.
    old_pos = env["purchase.order"].search([
        "|",
        ("name", "=", PO_ORIGIN),
        ("origin", "=", PO_ORIGIN),
    ])
    for po in old_pos:
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
            pass

    # Delete stale product (best-effort).
    for p in prods:
        try:
            env["stock.move.line"].search([("product_id", "=", p.id)]).unlink()
            env["stock.move"].search([("product_id", "=", p.id)]).unlink()
        except Exception:
            pass
    try:
        prods.mapped("product_tmpl_id").unlink()
    except Exception:
        pass


def _ensure_lost_location(env):
    """Create (or return) an inventory-type location 'Lost' under the
    main warehouse, so its complete_name becomes 'WH/Lost'.
    """
    Location = env["stock.location"]
    # Parent = the warehouse view location (usually 'Physical Locations/WH'
    # or similar). Safer: use the warehouse's view_location_id.
    wh = env["stock.warehouse"].search([("company_id", "=", env.company.id)], limit=1)
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    parent = wh.view_location_id if wh else False

    existing = Location.search([
        ("name", "=", LOST_LOCATION_NAME),
        ("location_id", "=", parent.id if parent else False),
    ], limit=1)
    if existing:
        if existing.usage != "inventory":
            existing.write({"usage": "inventory"})
        return existing

    vals = {
        "name": LOST_LOCATION_NAME,
        "usage": "inventory",
        "company_id": env.company.id,
    }
    if parent:
        vals["location_id"] = parent.id
    return Location.create(vals)


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")
    # The scrap_location_id / location_id fields on the Scrap dialog are
    # gated behind group_stock_multi_locations. The agent needs them
    # visible so they can type WH/Lost.
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    lost_loc = _ensure_lost_location(env)
    # Just to be safe: verify complete_name resolves to 'WH/Lost'.
    lost_loc._compute_complete_name()

    # Vendor.
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "ops@benchparts.example",
            "company_type": "company",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # Product — consumable (is_storable=False) so the scrap wizard
    # skips the availability check when source is 'Vendors'.
    product_tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": False,
        "tracking": "none",
        "list_price": 30.0,
        "standard_price": 18.0,
        "purchase_ok": True,
    })
    product = product_tmpl.product_variant_id

    # Create + confirm PO. Pin `name` so the generated receipt's
    # `origin` (which inherits from purchase.order.name, NOT from the
    # PO's own `origin` field) is deterministic for state-diff matching.
    po = env["purchase.order"].create({
        "name": PO_ORIGIN,
        "partner_id": vendor.id,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": product.id,
        "product_qty": DEMAND_QTY,
        "price_unit": 18.0,
        "name": PRODUCT_NAME,
    })
    po.button_confirm()

    # Confirm also generates the receipt; make sure it is assigned so
    # the Quantity column is editable. Also pin the picking name so
    # state-diff entity_keys of the created backorder are deterministic
    # (backorder_id normalizes to the parent picking's display name).
    for picking in po.picking_ids:
        if picking.state not in ("assigned", "done", "cancel"):
            try:
                picking.action_assign()
            except Exception:
                pass
        picking.write({"name": "R-BENCH-DMG-001"})
