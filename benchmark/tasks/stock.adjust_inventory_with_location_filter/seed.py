"""Seed inventory quants for the same product in two internal locations."""


def setup(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    quality_loc = env["stock.location"].search([
        ("name", "=", "WH/Quality"),
        ("usage", "=", "internal"),
    ], limit=1)
    if not quality_loc:
        quality_loc = env["stock.location"].create({
            "name": "WH/Quality",
            "usage": "internal",
            "location_id": warehouse.view_location_id.id,
        })

    product = env["product.product"].search([("name", "=", "Servo Motor A1")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Servo Motor A1",
            "type": "consu",
            "is_storable": True,
            "list_price": 180.0,
        })
        product = tmpl.product_variant_id

    env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "in", [stock_loc.id, quality_loc.id]),
    ]).unlink()

    env["stock.quant"]._update_available_quantity(product, stock_loc, 9.0)
    env["stock.quant"]._update_available_quantity(product, quality_loc, 7.0)
