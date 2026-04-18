"""Postcondition checks for inventory.cycle_count_two_locations_apply_selected_delta."""


def check(env):
    failures = []

    product = env["product.product"].search([
        ("name", "=", "Bench Cycle Count Rotor"),
    ], limit=1)
    if not product:
        return ["Product 'Bench Cycle Count Rotor' not found"]

    stock_loc = env["stock.location"].search([("complete_name", "=", "WH/Stock")], limit=1)
    input_loc = env["stock.location"].search([("complete_name", "=", "WH/Input")], limit=1)
    stock_quant = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", stock_loc.id),
    ], limit=1)
    input_quant = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", input_loc.id),
    ], limit=1)

    if not stock_quant or not input_quant:
        return ["Expected stock quants in WH/Stock and WH/Input were not found"]

    if abs(stock_quant.quantity - 12.0) > 1e-4:
        failures.append(
            f"WH/Stock quantity is {stock_quant.quantity}, expected 12.0"
        )
    if abs(input_quant.quantity - 6.0) > 1e-4:
        failures.append(
            f"WH/Input quantity is {input_quant.quantity}, expected unchanged 6.0"
        )

    adjustment_loc = env["stock.location"].search([("complete_name", "=", "Inventory adjustment")], limit=1)
    adjustment_quant = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", adjustment_loc.id),
    ], limit=1)
    if not adjustment_quant:
        failures.append("Expected inventory adjustment balancing quant was not found")
    elif abs(adjustment_quant.quantity - (-18.0)) > 1e-4:
        failures.append(
            f"Inventory adjustment quant is {adjustment_quant.quantity}, expected -18.0"
        )

    quants = env["stock.quant"].search([("product_id", "=", product.id)])
    if len(quants) != 3:
        failures.append(
            f"Expected exactly 3 quants for the product, found {len(quants)}"
        )

    return failures
