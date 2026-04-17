"""Postcondition checks for mrp.unbuild_product_partial."""


def check(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    orders = env["mrp.unbuild"].search([("product_id.display_name", "=", "Field Controller Kit")], order="id desc")
    if len(orders) != 1:
        return [f"Expected exactly one unbuild order, found {len(orders)}"]

    order = orders[0]
    failures = []
    if order.bom_id.code != "BOM-FCK-UNBUILD":
        failures.append(f"Unbuild order uses BoM {order.bom_id.code!r}, expected 'BOM-FCK-UNBUILD'")
    if abs(order.product_qty - 2.0) > 0.01:
        failures.append(f"Unbuild quantity is {order.product_qty}, expected 2.0")
    if order.state != "done":
        failures.append(f"Unbuild state is {order.state!r}, expected 'done'")

    def qty(product_name):
        product = env["product.product"].search([("name", "=", product_name)], limit=1)
        quants = env["stock.quant"].search([("product_id", "=", product.id), ("location_id", "=", stock_loc.id)])
        return sum(quants.mapped("quantity"))

    if abs(qty("Field Controller Kit") - 3.0) > 0.01:
        failures.append(f"Finished product stock is {qty('Field Controller Kit')}, expected 3.0")
    if qty("Sensor Board") < 4.0:
        failures.append("Sensor Board stock did not increase by the expected amount")
    if qty("Wiring Loom") < 2.0:
        failures.append("Wiring Loom stock did not increase by the expected amount")
    return failures
