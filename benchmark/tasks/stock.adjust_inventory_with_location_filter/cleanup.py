"""Clean up stock.adjust_inventory_with_location_filter artifacts."""


def cleanup(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    quality_loc = env["stock.location"].search([
        ("name", "=", "WH/Quality"),
        ("usage", "=", "internal"),
    ], limit=1)
    product = env["product.product"].search([("name", "=", "Servo Motor A1")], limit=1)
    if product and quality_loc:
        env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "in", [stock_loc.id, quality_loc.id]),
        ]).unlink()

