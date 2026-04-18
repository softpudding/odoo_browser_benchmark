"""Seed for stock.transfer_reserved_to_ready_partial_backorder.

Category 2 (HARD): policy_trap — partial validate + backorder dialog,
triggered through the Detailed Operations popup on the single move line.

Seeds:
  * Customer 'Bench Partial Cust'.
  * Storable product 'Bench Partial Item' (type='consu', is_storable=True,
    tracking='none') with 10 units on-hand at WH/Stock via stock.quant.
  * A confirmed outgoing delivery picking 'D-BENCH-PARTIAL-001' for 10
    units of Bench Partial Item to the customer, which is NOT yet
    reserved (state='confirmed'). The agent must click Check
    Availability to reserve before editing.

The agent must:
  1. Open the delivery, click Check Availability (picking → assigned,
     single move_line reserved with qty=10).
  2. Click Details on the move row to open the Detailed Operations
     popup, change Quantity 10 → 7, save the popup.
  3. Click Validate on the picking form.
  4. In the Create Backorder dialog, click 'Create Backorder' (primary,
     left) — not 'No Backorder' (secondary).

Failure modes the seed is designed to expose:
  * Agent skips Check Availability, tries to Validate directly and gets
    the availability wizard instead of the Create Backorder dialog.
  * Agent edits the inline Quantity cell in the picking form list and
    the cell never commits (Odoo 19 inline-cell-edit quirk).
  * Agent saves the popup without editing, or edits quantity but hits
    Cancel instead of Save.
  * Agent clicks 'No Backorder' on the dialog, so no backorder picking
    is created.
"""

ORIGIN = "D-BENCH-PARTIAL-001"
CUSTOMER_NAME = "Bench Partial Cust"
PRODUCT_NAME = "Bench Partial Item"
DEMAND_QTY = 10.0
ON_HAND_QTY = 10.0


def _cleanup(env):
    # Remove old pickings (original + backorder) referencing our origin /
    # customer.
    pickings = env["stock.picking"].search([
        "|",
        ("origin", "=", ORIGIN),
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

    # The Detailed Operations "Details" button on a move line is only
    # visible when the user has group_stock_multi_locations (or
    # tracking-lot / tracking-owner, or the product is tracked). We
    # need it visible so the agent can open the popup and edit Quantity
    # there. Grant the group to admin in seed.
    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    # Customer.
    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not customer:
        customer = env["res.partner"].create({
            "name": CUSTOMER_NAME,
            "email": "ops@benchpartial.example",
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
        "list_price": 40.0,
        "standard_price": 20.0,
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

    # Seed 10 units on-hand at WH/Stock.
    env["stock.quant"]._update_available_quantity(
        product, stock_location, ON_HAND_QTY
    )

    # Outgoing picking type for this warehouse.
    out_type = wh.out_type_id

    # Create the picking in a NOT-yet-assigned state. Use action_confirm so
    # procurement_group_id is set up and move.state='confirmed' — we
    # explicitly do NOT call action_assign so the agent must click Check
    # Availability in the UI.
    picking = env["stock.picking"].create({
        "picking_type_id": out_type.id,
        "partner_id": customer.id,
        "location_id": stock_location.id,
        "location_dest_id": customer_location.id,
        "origin": ORIGIN,
        # Pin the picking name so the state-diff entity_key
        # (backorder_id normalizes to parent picking.display_name) is
        # deterministic across runs.
        "name": ORIGIN,
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
    # Make sure reservation did NOT auto-run (some picking types have
    # reservation_method='at_confirm'). If it did, force-release the
    # reservation so the agent still has to click Check Availability.
    if picking.state == "assigned":
        try:
            picking.do_unreserve()
        except Exception:
            pass
    # Picking should now be in state 'confirmed' (Waiting / Ready to
    # reserve). The single move is in state 'confirmed' with 10 demand.
