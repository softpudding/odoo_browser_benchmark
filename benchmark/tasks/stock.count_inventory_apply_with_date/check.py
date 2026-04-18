"""Postcondition checks for stock.count_inventory_apply_with_date.

Verifies:
- The WH/Stock quant for 'Bench Stock Counter' is now quantity=25.
- An offsetting quant in the 'Inventory adjustment' virtual location was
  created (delta of -15 from initial 10).
- A stock.move in 'done' state exists for the product (the inventory
  adjustment move).
"""


PRODUCT_NAME = "Bench Stock Counter"


def check(env):
    failures = []

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    stock_loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not stock_loc:
        return ["Cannot find WH/Stock location"]

    stock_quant = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", stock_loc.id),
    ], limit=1)
    if not stock_quant:
        failures.append("Expected WH/Stock quant for product not found")
    elif abs(stock_quant.quantity - 25.0) > 1e-4:
        failures.append(
            f"WH/Stock quantity is {stock_quant.quantity}, expected 25.0"
        )

    adjustment_loc = env["stock.location"].search(
        [("complete_name", "=", "Inventory adjustment")], limit=1
    )
    if adjustment_loc:
        adj_quant = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", adjustment_loc.id),
        ], limit=1)
        if not adj_quant:
            failures.append(
                "Expected balancing quant in 'Inventory adjustment' location not found"
            )
        elif abs(adj_quant.quantity - (-25.0)) > 1e-4:
            failures.append(
                f"Inventory adjustment quant is {adj_quant.quantity}, expected -25.0"
            )

    # Verify an inventory adjustment stock.move exists for this product in done state.
    moves = env["stock.move"].search([
        ("product_id", "=", product.id),
        ("state", "=", "done"),
    ])
    if not moves:
        failures.append(
            "No completed stock.move found for product — Apply was not clicked"
        )

    return failures
