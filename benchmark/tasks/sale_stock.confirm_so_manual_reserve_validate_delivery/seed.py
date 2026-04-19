"""Seed a draft SO for a stockable product with on-hand stock.

Category: closed_loop_cross_module (MEDIUM).
The agent must confirm a draft SO, navigate from Sales to Inventory via the
Delivery smart button, explicitly Check Availability to reserve stock, and
Validate the delivery so all 5 units are delivered.
"""


def setup(env):
    # --- Partner ---
    partner = env["res.partner"].search(
        [("name", "=", "Bench SO Customer")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Bench SO Customer",
            "email": "bench.socust@example.com",
        })

    # --- Cleanup prior runs (target SOs and pickings for this customer) ---
    old_orders = env["sale.order"].search([
        ("partner_id", "=", partner.id),
    ])
    for so in old_orders:
        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
            if picking.state != "done":
                picking.unlink()
        if so.state in ("sale", "done"):
            so._action_cancel()
        so.unlink()

    # --- Product ---
    product = env["product.product"].search(
        [("name", "=", "Bench Stockable Product")], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": "Bench Stockable Product",
            "type": "consu",
            "list_price": 20.00,
            "standard_price": 10.00,
        })
        product = tmpl.product_variant_id
    # Make sure it's storable so pickings are created
    if not product.is_storable:
        product.product_tmpl_id.write({"type": "consu"})
        product.is_storable = True
    # Clear taxes for clean math
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    # --- Stock: 10 units on-hand in WH/Stock ---
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    # Wipe any existing quants on this product at this location so the seed
    # is idempotent.
    old_quants = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", stock_loc.id),
    ])
    for q in old_quants:
        q.with_context(inventory_mode=True).write({"inventory_quantity": 0})
        try:
            q.with_context(inventory_mode=True).action_apply_inventory()
        except Exception:
            pass

    env["stock.quant"].with_context(inventory_mode=True).create({
        "product_id": product.id,
        "location_id": stock_loc.id,
        "inventory_quantity": 10.0,
    }).action_apply_inventory()

    # --- Draft SO: 5 units of the product ---
    so = env["sale.order"].create({
        "partner_id": partner.id,
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": 5.0,
        "price_unit": 20.00,
        "tax_ids": [(5, 0, 0)],
    })
