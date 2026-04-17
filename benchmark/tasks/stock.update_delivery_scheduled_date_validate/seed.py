"""Seed a ready outgoing delivery for stock.update_delivery_scheduled_date_validate."""


def setup(env):
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Azure Interior", "email": "orders@azureinterior.com"})
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    products = {}
    for name, qty in [("Steel Bracket 12\"", 100), ("Copper Wire 100m", 40)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({"name": name, "type": "consu", "is_storable": True, "list_price": 10.0, "standard_price": 8.0})
            p = tmpl.product_variant_id
        else:
            if p.product_tmpl_id.type != "consu" or not p.product_tmpl_id.is_storable:
                p.product_tmpl_id.write({"type": "consu", "is_storable": True})
        products[name] = p
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": p.id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()
    for origin in ("BENCH-DEL-DATE-01", "BENCH-DEL-DATE-OTHER"):
        old_pickings = env["stock.picking"].search([("origin", "=", origin)])
        for pk in old_pickings:
            if pk.state not in ("cancel", "done"):
                pk.action_cancel()
            pk.unlink()
    picking_type = env["stock.picking.type"].search([("warehouse_id", "=", warehouse.id), ("code", "=", "outgoing")], limit=1)
    customer_loc = env.ref("stock.stock_location_customers")
    target = env["stock.picking"].create({
        "partner_id": partner.id,
        "picking_type_id": picking_type.id,
        "location_id": stock_loc.id,
        "location_dest_id": customer_loc.id,
        "origin": "BENCH-DEL-DATE-01",
        "scheduled_date": "2026-05-23 08:00:00",
    })
    env["stock.move"].create({"product_id": products['Steel Bracket 12"'].id, "product_uom_qty": 20, "product_uom": products['Steel Bracket 12"'].uom_id.id, "picking_id": target.id, "location_id": stock_loc.id, "location_dest_id": customer_loc.id})
    env["stock.move"].create({"product_id": products['Copper Wire 100m'].id, "product_uom_qty": 8, "product_uom": products['Copper Wire 100m'].uom_id.id, "picking_id": target.id, "location_id": stock_loc.id, "location_dest_id": customer_loc.id})
    target.action_confirm(); target.action_assign()
    distractor = env["stock.picking"].create({"partner_id": partner.id, "picking_type_id": picking_type.id, "location_id": stock_loc.id, "location_dest_id": customer_loc.id, "origin": "BENCH-DEL-DATE-OTHER"})
    env["stock.move"].create({"product_id": products['Steel Bracket 12"'].id, "product_uom_qty": 5, "product_uom": products['Steel Bracket 12"'].uom_id.id, "picking_id": distractor.id, "location_id": stock_loc.id, "location_dest_id": customer_loc.id})
    distractor.action_confirm(); distractor.action_assign()
