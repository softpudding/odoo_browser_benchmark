"""Postcondition checks for stock.adjust_inventory_count_apply_moves.

Validates:
  1. stock.quant.quantity for Bench Prod A at WH/Stock == 18.0.
  2. stock.quant.quantity for Bench Prod B at WH/Stock == 16.0.
  3. At least one stock.move with is_inventory=True exists for each
     adjusted product (delta -2 for A, +1 for B).
  4. No unexpected unlinks of the seeded products.
"""

PRODUCT_A = "Bench Prod A"
PRODUCT_B = "Bench Prod B"
EXPECTED_A = 18.0
EXPECTED_B = 16.0
DELTA_A = -2.0
DELTA_B = 1.0


def _find_stock_location(env):
    location = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location:
        location = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    return location


def check(env):
    failures = []

    location = _find_stock_location(env)
    if not location:
        return ["Cannot find WH/Stock location"]

    # Product lookup
    prod_a = env["product.product"].search(
        [("name", "=", PRODUCT_A)], limit=1
    )
    prod_b = env["product.product"].search(
        [("name", "=", PRODUCT_B)], limit=1
    )
    if not prod_a:
        failures.append(f"Product '{PRODUCT_A}' not found")
    if not prod_b:
        failures.append(f"Product '{PRODUCT_B}' not found")
    if failures:
        return failures

    # 1+2. Quantity after apply
    def _on_hand(product):
        quants = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", location.id),
        ])
        return sum(q.quantity for q in quants)

    qty_a = _on_hand(prod_a)
    qty_b = _on_hand(prod_b)

    if abs(qty_a - EXPECTED_A) > 1e-6:
        failures.append(
            f"Bench Prod A on-hand at WH/Stock is {qty_a}, expected "
            f"{EXPECTED_A} — did the agent change the Counted Quantity "
            f"cell to 18 and click Apply?"
        )
    if abs(qty_b - EXPECTED_B) > 1e-6:
        failures.append(
            f"Bench Prod B on-hand at WH/Stock is {qty_b}, expected "
            f"{EXPECTED_B} — did the agent change the Counted Quantity "
            f"cell to 16 and click Apply?"
        )

    # 3. stock.move records with is_inventory=True for each product
    moves_a = env["stock.move"].search([
        ("product_id", "=", prod_a.id),
        ("is_inventory", "=", True),
        ("state", "=", "done"),
    ])
    moves_b = env["stock.move"].search([
        ("product_id", "=", prod_b.id),
        ("is_inventory", "=", True),
        ("state", "=", "done"),
    ])
    if not moves_a:
        failures.append(
            "No done inventory-adjustment stock.move found for "
            "Bench Prod A (is_inventory=True) — Apply was not clicked or "
            "the adjustment failed to post"
        )
    else:
        # Net signed delta: moves going OUT of WH/Stock (location_id) are
        # negative adjustments, moves going INTO WH/Stock
        # (location_dest_id) are positive adjustments.
        net = 0.0
        for mv in moves_a:
            if mv.location_dest_id.id == location.id:
                net += mv.quantity or 0.0
            elif mv.location_id.id == location.id:
                net -= mv.quantity or 0.0
        if abs(net - DELTA_A) > 1e-6:
            failures.append(
                f"Bench Prod A inventory moves net delta is {net}, "
                f"expected {DELTA_A}"
            )

    if not moves_b:
        failures.append(
            "No done inventory-adjustment stock.move found for "
            "Bench Prod B (is_inventory=True) — Apply was not clicked or "
            "the adjustment failed to post"
        )
    else:
        net = 0.0
        for mv in moves_b:
            if mv.location_dest_id.id == location.id:
                net += mv.quantity or 0.0
            elif mv.location_id.id == location.id:
                net -= mv.quantity or 0.0
        if abs(net - DELTA_B) > 1e-6:
            failures.append(
                f"Bench Prod B inventory moves net delta is {net}, "
                f"expected {DELTA_B}"
            )

    return failures
