"""Postcondition checks for stock.create_physical_inventory_adjust_two_products.

Validates:
  1. stock.quant.quantity for Bench Prod X at WH/Stock == 12.0.
  2. stock.quant.quantity for Bench Prod Y at WH/Stock == 27.0.
  3. At least one stock.move with is_inventory=True, state='done' exists
     for each adjusted product, with net signed delta matching the
     expected adjustment (X: -3, Y: +2).
  4. No unexpected unlinks of the seeded products.
"""

PRODUCT_X = "Bench Prod X"
PRODUCT_Y = "Bench Prod Y"
EXPECTED_X = 12.0
EXPECTED_Y = 27.0
DELTA_X = -3.0
DELTA_Y = 2.0


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

    prod_x = env["product.product"].search(
        [("name", "=", PRODUCT_X)], limit=1
    )
    prod_y = env["product.product"].search(
        [("name", "=", PRODUCT_Y)], limit=1
    )
    if not prod_x:
        failures.append(f"Product '{PRODUCT_X}' not found")
    if not prod_y:
        failures.append(f"Product '{PRODUCT_Y}' not found")
    if failures:
        return failures

    # 1+2. Quantity after apply
    def _on_hand(product):
        quants = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", location.id),
        ])
        return sum(q.quantity for q in quants)

    qty_x = _on_hand(prod_x)
    qty_y = _on_hand(prod_y)

    if abs(qty_x - EXPECTED_X) > 1e-6:
        failures.append(
            f"Bench Prod X on-hand at WH/Stock is {qty_x}, expected "
            f"{EXPECTED_X} - did the agent change the Counted Quantity "
            f"cell to 12 and click Apply?"
        )
    if abs(qty_y - EXPECTED_Y) > 1e-6:
        failures.append(
            f"Bench Prod Y on-hand at WH/Stock is {qty_y}, expected "
            f"{EXPECTED_Y} - did the agent change the Counted Quantity "
            f"cell to 27 and click Apply?"
        )

    # 3. stock.move records with is_inventory=True, state='done' for
    # each product, with correct signed delta relative to WH/Stock.
    def _net_inventory_delta(product):
        moves = env["stock.move"].search([
            ("product_id", "=", product.id),
            ("is_inventory", "=", True),
            ("state", "=", "done"),
        ])
        if not moves:
            return None
        net = 0.0
        for mv in moves:
            if mv.location_dest_id.id == location.id:
                net += mv.quantity or 0.0
            elif mv.location_id.id == location.id:
                net -= mv.quantity or 0.0
        return net

    net_x = _net_inventory_delta(prod_x)
    if net_x is None:
        failures.append(
            "No done inventory-adjustment stock.move found for "
            "Bench Prod X (is_inventory=True, state='done') - Apply was "
            "not clicked or the adjustment failed to post"
        )
    elif abs(net_x - DELTA_X) > 1e-6:
        failures.append(
            f"Bench Prod X inventory moves net delta is {net_x}, "
            f"expected {DELTA_X}"
        )

    net_y = _net_inventory_delta(prod_y)
    if net_y is None:
        failures.append(
            "No done inventory-adjustment stock.move found for "
            "Bench Prod Y (is_inventory=True, state='done') - Apply was "
            "not clicked or the adjustment failed to post"
        )
    elif abs(net_y - DELTA_Y) > 1e-6:
        failures.append(
            f"Bench Prod Y inventory moves net delta is {net_y}, "
            f"expected {DELTA_Y}"
        )

    return failures
