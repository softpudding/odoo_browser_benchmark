"""Postcondition checks for stock.adjust_inventory_with_location_filter."""


def check(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id
    quality_loc = env["stock.location"].search([
        ("name", "=", "WH/Quality"),
        ("usage", "=", "internal"),
    ], limit=1)
    product = env["product.product"].search([("name", "=", "Servo Motor A1")], limit=1)
    if not (quality_loc and product):
        return ["Seeded product or quality location not found"]

    def qty_at(location):
        quants = env["stock.quant"].search([("product_id", "=", product.id), ("location_id", "=", location.id)])
        return sum(quants.mapped("quantity"))

    failures = []
    if abs(qty_at(stock_loc) - 18.0) > 0.01:
        failures.append(f"WH/Stock quantity is {qty_at(stock_loc)}, expected 18.0")
    if abs(qty_at(quality_loc) - 7.0) > 0.01:
        failures.append(f"WH/Quality quantity is {qty_at(quality_loc)}, expected 7.0")
    return failures
