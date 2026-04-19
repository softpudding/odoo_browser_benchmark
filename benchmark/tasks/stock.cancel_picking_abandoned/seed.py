"""Seed for stock.cancel_picking_abandoned.

Category: recovery_rollback (MEDIUM).

Seeds a Ready (assigned) outgoing delivery WH/OUT/BENCH-CANCEL for partner
'Bench Cancel Ship Co' with 3 units of 'Bench Cancel Prod' from WH/Stock to
the customer location. Demand=3, on-hand=3 so action_assign() fully reserves
the picking (state='assigned').

Capability tested: Cancel a picking via the statusbar 'Cancel' button +
confirm the resulting 'Are you sure you want to cancel this transfer?'
dialog. Pure cancel — no replacement, no serial, no validate — distinct from
row 338 (stock.cancel_picking_create_replacement_with_serial).

Failure modes the seed is designed to expose:
  * Agent dismisses the confirmation dialog instead of confirming it.
  * Agent clicks Validate instead of Cancel (picking would go to 'done').
  * Agent clicks Discard/Cancel in the breadcrumb instead of the statusbar
    action button.
  * Agent deletes the picking via cog menu instead of cancelling it.
"""

PICKING_NAME = "WH/OUT/BENCH-CANCEL"
CUSTOMER_NAME = "Bench Cancel Ship Co"
PRODUCT_NAME = "Bench Cancel Prod"
DEMAND_QTY = 3.0
ON_HAND_QTY = 3.0


def _cleanup(env):
    # Remove any prior pickings with our pinned name or our customer.
    pickings = env["stock.picking"].with_context(active_test=False).search([
        "|",
        ("name", "=", PICKING_NAME),
        "&",
        ("partner_id.name", "=", CUSTOMER_NAME),
        ("picking_type_id.code", "=", "outgoing"),
    ])
    # Children (backorders) first.
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

    # Stale product (and all moves/quants/lines referencing it).
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
            "email": "ops@benchcancelship.example",
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
        "list_price": 20.0,
        "standard_price": 12.0,
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

    # Seed 3 units on-hand at WH/Stock.
    env["stock.quant"]._update_available_quantity(
        product, stock_location, ON_HAND_QTY
    )

    # Outgoing picking type for this warehouse.
    out_type = wh.out_type_id

    # Create the picking with a pinned name so the agent can find it
    # deterministically by WH/OUT/BENCH-CANCEL.
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
    # Reserve so state='assigned' (Ready).
    picking.action_assign()
    if picking.state != "assigned":
        picking.move_ids._action_assign()

    assert picking.state == "assigned", (
        f"Seed expected picking.state='assigned', got {picking.state!r}"
    )
    assert picking.name == PICKING_NAME, (
        f"Seed expected picking.name={PICKING_NAME!r}, got {picking.name!r}"
    )
