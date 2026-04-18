"""Postcondition checks for stock.adjust_inventory_with_location_filter.

Verifies:
- The Shelf A quant for 'Bench Multi Loc Product' is now quantity=42.
- The Shelf B quant for the same product is still quantity=30 (unchanged).
- The product's total on-hand across Shelf A + Shelf B is 72.
- A completed stock.move exists for the product (the inventory adjustment).
"""


PRODUCT_NAME = "Bench Multi Loc Product"
SHELF_A_COMPLETE = "WH/Stock/Shelf A"
SHELF_B_COMPLETE = "WH/Stock/Shelf B"


def check(env):
    failures = []

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    shelf_a = env["stock.location"].search(
        [("complete_name", "=", SHELF_A_COMPLETE)], limit=1
    )
    shelf_b = env["stock.location"].search(
        [("complete_name", "=", SHELF_B_COMPLETE)], limit=1
    )
    if not shelf_a:
        failures.append(f"Cannot find {SHELF_A_COMPLETE} location")
    if not shelf_b:
        failures.append(f"Cannot find {SHELF_B_COMPLETE} location")
    if failures:
        return failures

    q_a = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", shelf_a.id),
    ], limit=1)
    q_b = env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", shelf_b.id),
    ], limit=1)

    if not q_a:
        failures.append(f"Expected {SHELF_A_COMPLETE} quant not found")
    elif abs(q_a.quantity - 42.0) > 1e-4:
        failures.append(
            f"{SHELF_A_COMPLETE} quantity is {q_a.quantity}, expected 42.0"
        )

    if not q_b:
        failures.append(f"Expected {SHELF_B_COMPLETE} quant not found")
    elif abs(q_b.quantity - 30.0) > 1e-4:
        failures.append(
            f"{SHELF_B_COMPLETE} quantity is {q_b.quantity}, expected 30.0 "
            f"(must remain unchanged)"
        )

    # Total on-hand (across both internal shelves) must be 42 + 30 = 72.
    if q_a and q_b:
        total = q_a.quantity + q_b.quantity
        if abs(total - 72.0) > 1e-4:
            failures.append(
                f"Combined Shelf A + Shelf B on-hand is {total}, expected 72.0"
            )

    # Verify an inventory adjustment stock.move exists in done state.
    moves = env["stock.move"].search([
        ("product_id", "=", product.id),
        ("state", "=", "done"),
    ])
    if not moves:
        failures.append(
            "No completed stock.move found for product — Apply was not clicked"
        )

    return failures
