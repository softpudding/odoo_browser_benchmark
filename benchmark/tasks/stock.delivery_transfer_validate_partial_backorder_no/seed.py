"""Seed for stock.delivery_transfer_validate_partial_backorder_no.

Category 2 (MEDIUM): policy_trap — partial validate where the agent must
click the SECONDARY 'No Backorder' button on the Create Backorder dialog
instead of the default/primary 'Create Backorder' button.

Seeds:
  * Customer 'Bench Ship Co'.
  * Storable product 'Bench Pick Item' (type='consu', is_storable=True,
    tracking='none') with 5 units on-hand at WH/Stock via stock.quant.
  * A Ready (reserved / assigned) outgoing delivery picking
    'WH/OUT/BENCH-BACKORDER-NO' for 5 units of Bench Pick Item to the
    customer. The picking is action_confirm + action_assign'd so its
    state='assigned' and the single move line is fully reserved with
    qty=5.

The agent must:
  1. Open the delivery.
  2. Edit the inline Done qty cell on the single move line: 5 -> 3,
     commit with Tab.
  3. Click Validate.
  4. On the 'Create Backorder?' dialog, click the SECONDARY
     'No Backorder' button (NOT the primary 'Create Backorder').

Failure modes the seed is designed to expose:
  * Agent clicks the primary/default 'Create Backorder' button, which
    creates an unwanted backorder for 2 units (main trap — the default
    is the WRONG choice here).
  * Agent edits the inline Done cell but the change doesn't persist
    (Odoo 19 inline-cell-edit quirk — but with on-hand=5 and demand=5,
    validate still succeeds with full qty=5 if the edit lost, and no
    dialog appears at all, so state=done but qty_done=5 → fails check).
"""

PICKING_NAME = "WH/OUT/BENCH-BACKORDER-NO"
CUSTOMER_NAME = "Bench Ship Co"
PRODUCT_NAME = "Bench Pick Item"
DEMAND_QTY = 5.0
ON_HAND_QTY = 5.0


def _cleanup(env):
    # Remove old pickings (original + any backorders) referencing our
    # name / customer.
    pickings = env["stock.picking"].search([
        "|",
        ("name", "=", PICKING_NAME),
        "&",
        ("partner_id.name", "=", CUSTOMER_NAME),
        ("picking_type_id.code", "=", "outgoing"),
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

    # Stale quants + move lines on the product.
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

    # Customer.
    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not customer:
        customer = env["res.partner"].create({
            "name": CUSTOMER_NAME,
            "email": "ops@benchshipco.example",
            "company_type": "company",
            "customer_rank": 1,
        })
    else:
        customer.write({"customer_rank": max(customer.customer_rank, 1)})

    # Storable product so stock.quant reservations are meaningful.
    product_tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 30.0,
        "standard_price": 15.0,
        "sale_ok": True,
        "purchase_ok": False,
    })
    product = product_tmpl.product_variant_id

    # Locations.
    wh = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    stock_location = wh.lot_stock_id
    customer_location = env.ref("stock.stock_location_customers")

    # Seed 5 units on-hand at WH/Stock.
    env["stock.quant"]._update_available_quantity(
        product, stock_location, ON_HAND_QTY
    )

    # Outgoing picking type for this warehouse.
    out_type = wh.out_type_id

    # Create the picking with a pinned name so we can find it
    # deterministically and so backorder-checking entity_keys resolve to
    # that same display_name if a (bug-path) backorder were ever made.
    picking = env["stock.picking"].create({
        "picking_type_id": out_type.id,
        "partner_id": customer.id,
        "location_id": stock_location.id,
        "location_dest_id": customer_location.id,
        "origin": PICKING_NAME,
        "name": PICKING_NAME,
    })
    env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": DEMAND_QTY,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": stock_location.id,
        "location_dest_id": customer_location.id,
    })

    picking.action_confirm()
    # Reserve (assign) the picking so its state is 'assigned' and the
    # single move line has a reserved qty of 5 (Done auto-fills to 5).
    # The agent does NOT need to click Check Availability.
    picking.action_assign()
    # Belt-and-suspenders: ensure state is 'assigned' (reserved full 5).
    if picking.state != "assigned":
        # If for some reason the assignment failed, force re-assign.
        picking.move_ids._action_assign()
