"""Seed for sale_stock.partial_stock_warning_confirm_anyway.

Category: Policy trap (wizard) — HARD.

Creates:
    - Storable product 'Bench Limited Widget' with exactly 2 units on-hand
      in main stock location.
    - Customer 'Bench Warehouse Co'.
    - Draft quotation S-BENCH-STK-001 with one line: Bench Limited Widget x 10.

The agent must confirm the SO despite the under-reservation, navigate to the
delivery, validate with Done=2, and pick 'Create Backorder' in the wizard.
"""


def setup(env):
    # --- Partner ---
    partner = env["res.partner"].search(
        [("name", "=", "Bench Warehouse Co")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Bench Warehouse Co",
            "email": "ops@benchwarehouse.co",
        })

    # --- Cleanup prior runs ---
    old_orders = env["sale.order"].search([
        ("client_order_ref", "=", "S-BENCH-STK-001"),
    ])
    for so in old_orders:
        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
            # Also clean up backorders that may have been created
            bo_children = env["stock.picking"].search([
                ("backorder_id", "=", picking.id),
            ])
            for bo in bo_children:
                if bo.state not in ("cancel", "done"):
                    bo.action_cancel()
                try:
                    bo.unlink()
                except Exception:
                    pass
            try:
                picking.unlink()
            except Exception:
                pass
        if so.state in ("sale", "done"):
            so._action_cancel()
        so.unlink()

    # --- Product ---
    product_name = "Bench Limited Widget"
    product = env["product.product"].search(
        [("name", "=", product_name)], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": product_name,
            "type": "consu",
            "list_price": 120.00,
            "standard_price": 80.00,
        })
        product = tmpl.product_variant_id
    else:
        if product.product_tmpl_id.type != "consu":
            product.product_tmpl_id.write({"type": "consu"})

    # Must be storable to enable stock tracking / reservation warnings
    if hasattr(product, "is_storable"):
        product.is_storable = True
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    # --- Set on-hand quantity = 2 ---
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    # First clear any stray quants for this product in that location.
    existing_quants = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", stock_loc.id),
    ])
    for q in existing_quants:
        q.with_context(inventory_mode=True).write({"inventory_quantity": 0})
        try:
            q.with_context(inventory_mode=True).action_apply_inventory()
        except Exception:
            pass

    # Set on-hand = 5 (more than what the agent should ship, less than ordered).
    # Reservation will auto-fill Done = 5 on the delivery; the agent must
    # MANUALLY change Done to 2 before validating, then choose
    # Create Backorder for the remaining 8 units of the original demand
    # (note: backorder demand will actually be 10 - 2 = 8).
    env["stock.quant"].with_context(inventory_mode=True).create({
        "product_id": product.id,
        "location_id": stock_loc.id,
        "inventory_quantity": 5,
    }).action_apply_inventory()

    # --- Draft SO ---
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "S-BENCH-STK-001",
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": 10,
        "price_unit": 120.00,
        "tax_ids": [(5, 0, 0)],
    })
