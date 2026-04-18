"""Seed for delivery.set_third_party_carrier_print_label.

Category: deep_ui_interaction (MEDIUM).

Creates a confirmed customer-delivery picking sourced from sale order
S-BENCH-DLV-002 (one Bench Express Crate x 3, reserved). The agent must
configure a new fixed-price carrier 'Bench Express', apply it to the
picking, type a tracking reference, validate the picking, and click the
'Print' header button. The picking ends in state=done with a non-null
carrier_tracking_ref.
"""


def setup(env):
    # --- Cleanup prior runs ---
    for ref in ("S-BENCH-DLV-002",):
        for so in env["sale.order"].search([("client_order_ref", "=", ref)]):
            for picking in so.picking_ids:
                if picking.state not in ("cancel", "done"):
                    picking.action_cancel()
                picking.unlink()
            if so.state in ("sale", "done"):
                so._action_cancel()
            so.unlink()

    # Loose pickings with the same origin (in case prior runs created free-standing
    # pickings outside an SO).
    for picking in env["stock.picking"].search([("origin", "=", "S-BENCH-DLV-002")]):
        if picking.state not in ("cancel", "done"):
            picking.action_cancel()
        picking.unlink()

    env["delivery.carrier"].with_context(active_test=False).search([
        ("name", "=", "Bench Express"),
    ]).unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", ["Bench Express Crate", "Bench Express Shipping"]),
    ]).unlink()

    # --- Partner ---
    partner = env["res.partner"].search([("name", "=", "Bench Express Customer")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Bench Express Customer",
            "email": "ship@bench-express.example.com",
        })

    # --- Storable product with on-hand stock ---
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    product_tmpl = env["product.template"].create({
        "name": "Bench Express Crate",
        "type": "consu",
        "is_storable": True,
        "list_price": 50.0,
        "standard_price": 30.0,
        "weight": 4.0,
    })
    product = product_tmpl.product_variant_id
    product_tmpl.write({"taxes_id": [(5, 0, 0)]})

    # Make sure there is enough on-hand to reserve 3 units.
    env["stock.quant"].with_context(inventory_mode=True).create({
        "product_id": product.id,
        "location_id": stock_loc.id,
        "inventory_quantity": 25.0,
    }).action_apply_inventory()

    # --- Sale order, confirmed (creates the delivery picking automatically) ---
    # Force the SO name so the picking's `origin` is the deterministic
    # 'S-BENCH-DLV-002' (origin defaults to the SO name, not the
    # client_order_ref). The agent uses the customer reference shown on the
    # picking form to identify the right transfer.
    so = env["sale.order"].create({
        "name": "S-BENCH-DLV-002",
        "partner_id": partner.id,
        "client_order_ref": "S-BENCH-DLV-002",
        "order_line": [(0, 0, {
            "product_id": product.id,
            "name": "Bench Express Crate",
            "product_uom_qty": 3,
            "price_unit": 50.0,
            "tax_ids": [(5, 0, 0)],
        })],
    })
    so.action_confirm()

    # Reserve the picking so it shows up as Ready.
    for picking in so.picking_ids:
        picking.action_assign()
