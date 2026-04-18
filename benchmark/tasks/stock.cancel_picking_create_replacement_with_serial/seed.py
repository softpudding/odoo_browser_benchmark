"""Seed for stock.cancel_picking_create_replacement_with_serial.

Category 4 (HARD): recovery / rollback.
Creates a ready vendor receipt (R-BENCH-CANCEL-001) with a
non-serial-tracked product for Bench Supplier Inc, qty 5, which
the agent must CANCEL in Part A. In Part B/C/D the agent creates a
brand-new receipt from scratch for the same vendor, adds a single
line for a *serial-tracked* product (Bench Serial Widget, qty=2),
then opens Detailed Operations and enters TWO distinct serials
BS-001 / BS-002 (one per move_line, qty 1 each) before validating.

Failure modes the seed is designed to expose:

* Agent skips the Cancel on the original and just creates the new
  receipt, so the original is still 'assigned'/'ready'.
* Agent enters only BS-001 (one move_line of qty 2) and validates;
  BS-002 is missing. This is the hard BU trap.
"""

ORIGINAL_ORIGIN = "R-BENCH-CANCEL-001"
VENDOR_NAME = "Bench Supplier Inc"
WRONG_PRODUCT_NAME = "Bench Hardware Item"
SERIAL_PRODUCT_NAME = "Bench Serial Widget"
DEMAND_WRONG = 5.0


def _cleanup(env):
    # Any prior replacement receipts or test pickings referencing our vendor / products.
    pickings = env["stock.picking"].search([
        "|",
        ("origin", "=", ORIGINAL_ORIGIN),
        ("partner_id.name", "=", VENDOR_NAME),
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

    # Delete any stale lots/move_lines for our products.
    for pname in (WRONG_PRODUCT_NAME, SERIAL_PRODUCT_NAME):
        prods = env["product.product"].search([("name", "=", pname)])
        env["stock.move.line"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.move"].search([("product_id", "in", prods.ids)]).unlink()
        env["stock.lot"].search([("product_id", "in", prods.ids)]).unlink()
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    # Remove our specific stale lots by name in case they're orphaned.
    stale_lots = env["stock.lot"].search([("name", "in", ["BS-001", "BS-002"])])
    if stale_lots:
        try:
            stale_lots.unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_production_lot")

    # Receipts picking type: allow on-the-fly lot/serial creation so the popup
    # exposes lot_name + autocomplete Create.
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
            "email": "orders@benchsupplier.example",
            "supplier_rank": 1,
            "company_type": "company",
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # Products.
    wrong_tmpl = env["product.template"].create({
        "name": WRONG_PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 50.0,
        "standard_price": 30.0,
    })
    wrong_product = wrong_tmpl.product_variant_id

    serial_tmpl = env["product.template"].create({
        "name": SERIAL_PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "serial",
        "list_price": 250.0,
        "standard_price": 120.0,
    })
    serial_product = serial_tmpl.product_variant_id

    # Locations.
    location_supplier = env.ref("stock.stock_location_suppliers")
    location_stock = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location_stock:
        location_stock = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )

    # ------------------------------------------------------------------
    # Original ready receipt (Part A target).
    # ------------------------------------------------------------------
    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "partner_id": vendor.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
        "origin": ORIGINAL_ORIGIN,
    })
    env["stock.move"].create({
        "product_id": wrong_product.id,
        "product_uom_qty": DEMAND_WRONG,
        "product_uom": wrong_product.uom_id.id,
        "picking_id": picking.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
    })

    picking.action_confirm()
    picking.action_assign()
    # Leave it READY (assigned). The agent must click Cancel.
