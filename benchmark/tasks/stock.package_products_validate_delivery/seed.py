"""Seed for stock.package_products_validate_delivery."""


def setup(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    customer_loc = env.ref("stock.stock_location_customers")

    partner = env["res.partner"].search([("name", "=", "Package Harbor")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Package Harbor"})

    env["stock.picking"].search([("origin", "in", ["BENCH-PACK-DEL-01", "BENCH-PACK-DEL-OTHER"])]).unlink()
    env["product.template"].search([("name", "in", ["Packed Valve Kit", "Packed Sensor Cable"])]).unlink()

    valve = env["product.product"].create({
        "name": "Packed Valve Kit",
        "type": "consu",
        "is_storable": True,
        "list_price": 40.0,
    })
    cable = env["product.product"].create({
        "name": "Packed Sensor Cable",
        "type": "consu",
        "is_storable": True,
        "list_price": 15.0,
    })

    for product, qty in [(valve, 20.0), (cable, 20.0)]:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    picking_type = env["stock.picking.type"].search([
        ("warehouse_id", "=", warehouse.id),
        ("code", "=", "outgoing"),
    ], limit=1)

    target = env["stock.picking"].create({
        "partner_id": partner.id,
        "picking_type_id": picking_type.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
        "origin": "BENCH-PACK-DEL-01",
    })
    env["stock.move"].create({
        "product_id": valve.id,
        "product_uom_qty": 4.0,
        "product_uom": valve.uom_id.id,
        "picking_id": target.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
    })
    env["stock.move"].create({
        "product_id": cable.id,
        "product_uom_qty": 6.0,
        "product_uom": cable.uom_id.id,
        "picking_id": target.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
    })
    target.action_confirm()
    target.action_assign()

    distractor = env["stock.picking"].create({
        "partner_id": partner.id,
        "picking_type_id": picking_type.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
        "origin": "BENCH-PACK-DEL-OTHER",
    })
    env["stock.move"].create({
        "product_id": valve.id,
        "product_uom_qty": 1.0,
        "product_uom": valve.uom_id.id,
        "picking_id": distractor.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
    })
    distractor.action_confirm()
    distractor.action_assign()
