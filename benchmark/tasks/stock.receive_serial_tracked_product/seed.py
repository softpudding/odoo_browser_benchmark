"""Seed an incoming receipt for a serial-tracked product."""


def setup(env):
    ref = "BENCH-SERIAL-REC-01"
    supplier_loc = env.ref("stock.stock_location_suppliers")
    stock_loc = env["stock.location"].search([("usage", "=", "internal")], limit=1)
    picking_type = env["stock.picking.type"].search([("code", "=", "incoming")], limit=1)
    lot_group = env.ref("stock.group_production_lot")
    admin_user = env.ref("base.user_admin")
    if lot_group not in admin_user.group_ids:
        admin_user.group_ids = [(4, lot_group.id)]

    env["stock.lot"].search([("name", "in", ["CSX-001", "CSX-002", "CSX-003"])]).unlink()
    picks = env["stock.picking"].search([("origin", "=", ref)])
    for pick in picks:
        if pick.state not in ("cancel", "done"):
            pick.action_cancel()
        pick.unlink()

    product = env["product.product"].search([("name", "=", "Calibration Scanner X")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Calibration Scanner X",
            "type": "consu",
            "is_storable": True,
            "tracking": "serial",
            "list_price": 320.0,
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({"tracking": "serial", "type": "consu", "is_storable": True})

    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "location_id": supplier_loc.id,
        "location_dest_id": stock_loc.id,
        "origin": ref,
    })
    env["stock.move"].create({
        "product_id": product.id,
        "product_uom_qty": 3.0,
        "product_uom": product.uom_id.id,
        "picking_id": picking.id,
        "location_id": supplier_loc.id,
        "location_dest_id": stock_loc.id,
    })
    picking.action_confirm()
    picking.action_assign()
