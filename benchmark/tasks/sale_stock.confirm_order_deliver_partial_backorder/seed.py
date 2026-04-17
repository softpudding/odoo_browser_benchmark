"""Seed a draft SO with 3 product lines for the partial-delivery backorder task.

Category 3 (HARD): The agent must confirm a draft SO, navigate to its
delivery via the smart button, set partial Done quantities on 3 move
lines, validate, and choose "Create Backorder" in the wizard dialog.
Capability tested: cross-module Sales -> Stock navigation, inline
quantity editing, backorder wizard interaction.
"""


def setup(env):
    # --- Partners ---
    partner = env["res.partner"].search(
        [("name", "=", "Westfield Manufacturing")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Westfield Manufacturing",
            "email": "orders@westfieldmfg.com",
        })

    distractor_partner = env["res.partner"].search(
        [("name", "=", "Westfield Metals")], limit=1
    )
    if not distractor_partner:
        distractor_partner = env["res.partner"].create({
            "name": "Westfield Metals",
            "email": "sales@westfieldmetals.com",
        })

    # --- Cleanup prior runs ---
    for ref in ("BENCH-SO-BACK", "BENCH-SO-BACK-DIST"):
        old_orders = env["sale.order"].search([
            ("client_order_ref", "=", ref),
        ])
        for so in old_orders:
            # Cancel deliveries first
            for picking in so.picking_ids:
                if picking.state not in ("cancel", "done"):
                    picking.action_cancel()
            if so.state in ("sale", "done"):
                so._action_cancel()
            so.unlink()

    # --- Products ---
    products = {}
    for name, price in [
        ("Precision Bearing Kit", 75.00),
        ("Stainless Steel Rod 2m", 32.00),
        ("Titanium Bolt Set M12", 48.00),
    ]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
            p = tmpl.product_variant_id
        else:
            if p.product_tmpl_id.type != "consu":
                p.product_tmpl_id.write({"type": "consu"})
        p.is_storable = True
        # Clear taxes on product template
        p.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})
        products[name] = p

    # Ensure enough stock for delivery reservation
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    for name, qty in [
        ("Precision Bearing Kit", 100),
        ("Stainless Steel Rod 2m", 100),
        ("Titanium Bolt Set M12", 100),
    ]:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": products[name].id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    # --- Target draft SO: "BENCH-SO-BACK" ---
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "BENCH-SO-BACK",
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Precision Bearing Kit"].id,
        "product_uom_qty": 25,
        "price_unit": 75.00,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Stainless Steel Rod 2m"].id,
        "product_uom_qty": 40,
        "price_unit": 32.00,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Titanium Bolt Set M12"].id,
        "product_uom_qty": 20,
        "price_unit": 48.00,
        "tax_ids": [(5, 0, 0)],
    })

    # --- Distractor draft SO: "BENCH-SO-BACK-DIST" ---
    dist_so = env["sale.order"].create({
        "partner_id": distractor_partner.id,
        "client_order_ref": "BENCH-SO-BACK-DIST",
    })
    env["sale.order.line"].create({
        "order_id": dist_so.id,
        "product_id": products["Precision Bearing Kit"].id,
        "product_uom_qty": 10,
        "price_unit": 75.00,
        "tax_ids": [(5, 0, 0)],
    })
