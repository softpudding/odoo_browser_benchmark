"""Postcondition checks for stock.adjust_inventory_quantities.

Validates that on-hand quantities for the three target products were
updated to the correct values, and that the two distractor products
were left unchanged.
"""


def check(env):
    failures = []

    location = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location:
        location = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    if not location:
        return ["Cannot find WH/Stock location"]

    def get_qty(product_name):
        product = env["product.product"].search([("name", "=", product_name)], limit=1)
        if not product:
            return None
        quants = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", location.id),
        ])
        return sum(q.quantity for q in quants)

    # Products that must be adjusted
    expected_adjusted = {
        "Steel Bracket 12\"": 45.0,
        "Copper Wire 100m": 120.0,
        "Safety Harness XL": 8.0,
    }
    for name, expected_qty in expected_adjusted.items():
        qty = get_qty(name)
        if qty is None:
            failures.append(f"Product '{name}' not found")
        elif abs(qty - expected_qty) > 0.01:
            failures.append(
                f"Product '{name}': on-hand qty is {qty}, expected {expected_qty}"
            )

    # Distractor products that must NOT be changed
    expected_unchanged = {
        "Latex Work Gloves L": 30.0,
        "Hard Hat Yellow": 15.0,
    }
    for name, expected_qty in expected_unchanged.items():
        qty = get_qty(name)
        if qty is None:
            failures.append(f"Distractor product '{name}' not found — was it deleted?")
        elif abs(qty - expected_qty) > 0.01:
            failures.append(
                f"Distractor product '{name}' was changed: qty is {qty}, should still be {expected_qty}"
            )

    return failures
