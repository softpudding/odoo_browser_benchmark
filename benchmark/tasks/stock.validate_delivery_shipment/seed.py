"""Seed a ready outgoing delivery for the validate-delivery task.

Category 2 (MEDIUM): The agent must locate the correct outgoing
delivery among two similar ones, set done quantities on two move lines,
and validate. Capability tested: stock delivery validation (distinct
from receipt validation tasks).
"""


def setup(env):
    # --- Partner ---
    partner = env["res.partner"].search(
        [("name", "=", "Azure Interior")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Azure Interior",
            "email": "orders@azureinterior.com",
        })

    # --- Ensure products are stockable and have on-hand stock ---
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    products = {}
    for name, qty in [("Steel Bracket 12\"", 100), ("Copper Wire 100m", 40)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,
                "list_price": 10.0,
                "standard_price": 8.0,
            })
            p = tmpl.product_variant_id
        else:
            if p.product_tmpl_id.type != "consu" or not p.product_tmpl_id.is_storable:
                p.product_tmpl_id.write({
                    "type": "consu",
                    "is_storable": True,
                })
        products[name] = p
        # Ensure enough on-hand to satisfy the planned delivery
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": p.id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    # --- Cleanup prior runs (pickings) ---
    for origin in ("BENCH-DEL-01", "BENCH-DEL-OTHER"):
        old_pickings = env["stock.picking"].search([("origin", "=", origin)])
        for pk in old_pickings:
            if pk.state not in ("cancel", "done"):
                pk.action_cancel()
            pk.unlink()

    # --- Create a Delivery Order picking type ---
    picking_type = env["stock.picking.type"].search([
        ("warehouse_id", "=", warehouse.id),
        ("code", "=", "outgoing"),
    ], limit=1)
    customer_loc = env.ref("stock.stock_location_customers")

    # --- Create target delivery BENCH-DEL-01 ---
    target = env["stock.picking"].create({
        "partner_id": partner.id,
        "picking_type_id": picking_type.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
        "origin": "BENCH-DEL-01",
    })
    env["stock.move"].create({
        "name": "Steel Bracket 12\"",
        "product_id": products["Steel Bracket 12\""].id,
        "product_uom_qty": 20,
        "product_uom": products["Steel Bracket 12\""].uom_id.id,
        "picking_id": target.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
    })
    env["stock.move"].create({
        "name": "Copper Wire 100m",
        "product_id": products["Copper Wire 100m"].id,
        "product_uom_qty": 8,
        "product_uom": products["Copper Wire 100m"].uom_id.id,
        "picking_id": target.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
    })
    target.action_confirm()
    target.action_assign()

    # --- Distractor delivery BENCH-DEL-OTHER (must remain untouched) ---
    distractor = env["stock.picking"].create({
        "partner_id": partner.id,
        "picking_type_id": picking_type.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
        "origin": "BENCH-DEL-OTHER",
    })
    env["stock.move"].create({
        "name": "Steel Bracket 12\"",
        "product_id": products["Steel Bracket 12\""].id,
        "product_uom_qty": 5,
        "product_uom": products["Steel Bracket 12\""].uom_id.id,
        "picking_id": distractor.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
    })
    distractor.action_confirm()
    distractor.action_assign()
