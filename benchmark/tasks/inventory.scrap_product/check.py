"""Postcondition checks for inventory.scrap_product.

Validates that:
1. A scrap order exists for Steel Bracket 12" with quantity 5
2. The scrap order is in 'done' state
"""


def check(env):
    failures = []

    # Find the product
    product = env["product.product"].search([
        ("name", "=", "Steel Bracket 12\""),
    ], limit=1)

    if not product:
        return ["Product 'Steel Bracket 12\"' not found"]

    # Find scrap orders for this product
    scraps = env["stock.scrap"].search([
        ("product_id", "=", product.id),
    ])

    if not scraps:
        return ["No scrap order found for product 'Steel Bracket 12\"'"]

    # Check that at least one scrap order has quantity 5 and is done
    found = False
    for scrap in scraps:
        if scrap.scrap_qty == 5.0 and scrap.state == "done":
            found = True
            break

    if not found:
        failures.append(
            f"No scrap order with quantity 5.0 and state 'done' found. "
            f"Found {len(scraps)} scrap order(s): "
            + ", ".join(f"qty={s.scrap_qty}, state={s.state}" for s in scraps)
        )

    return failures