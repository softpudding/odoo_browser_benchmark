"""Seed a completed receipt used as the starting point for a scrap flow."""


def setup(env):
    ref = "BENCH-SCRAP-REC-01"
    supplier_loc = env.ref("stock.stock_location_suppliers")
    stock_loc = env["stock.location"].search([("usage", "=", "internal")], limit=1)
    picking_type = env["stock.picking.type"].search([("code", "=", "incoming")], limit=1)

    env["stock.scrap"].search([("origin", "=", ref)]).unlink()
    old_picks = env["stock.picking"].search([("origin", "=", ref)])
    for pick in old_picks:
        if pick.state not in ("cancel", "done"):
            pick.action_cancel()
        pick.unlink()

    product = env["product.product"].search([("name", "=", "Steel Bracket 12\"")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Steel Bracket 12\"",
            "type": "consu",
            "is_storable": True,
            "list_price": 25.0,
        })
        product = tmpl.product_variant_id

    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "location_id": supplier_loc.id,
        "location_dest_id": stock_loc.id,
        "origin": ref,
    })
    move = env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": 12.0,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": supplier_loc.id,
        "location_dest_id": stock_loc.id,
    })
    picking.action_confirm()
    picking.action_assign()
    move.quantity = 12.0
    picking.button_validate()
