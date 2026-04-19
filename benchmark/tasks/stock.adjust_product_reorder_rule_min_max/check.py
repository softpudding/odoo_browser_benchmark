"""Postcondition checks for stock.adjust_product_reorder_rule_min_max.

Validates:
  1. Exactly one stock.warehouse.orderpoint exists for 'Bench Reorder Item'.
  2. That orderpoint has product_min_qty == 5.0 and product_max_qty == 20.0.
  3. Its location_id is the WH/Stock internal location.
  4. Product itself was not mutated (name/type/is_storable unchanged).
"""

PRODUCT_NAME = "Bench Reorder Item"
EXPECTED_MIN = 5.0
EXPECTED_MAX = 20.0


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

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    # 4. Product integrity
    if product.type != "consu":
        failures.append(
            f"Product type is '{product.type}', expected 'consu' — agent "
            f"may have edited the product itself"
        )
    if not product.is_storable:
        failures.append(
            "Product is_storable is False, expected True — agent may have "
            "edited the storable flag on the product"
        )

    # 1. Exactly one orderpoint
    orderpoints = env["stock.warehouse.orderpoint"].with_context(
        active_test=False
    ).search([("product_id", "=", product.id)])
    if len(orderpoints) == 0:
        return failures + [
            f"No stock.warehouse.orderpoint found for '{PRODUCT_NAME}' — "
            f"agent never created the reordering rule"
        ]
    if len(orderpoints) > 1:
        failures.append(
            f"Expected exactly 1 stock.warehouse.orderpoint for "
            f"'{PRODUCT_NAME}', found {len(orderpoints)}: "
            f"{orderpoints.mapped('name')}"
        )
    op = orderpoints[:1]

    # Orderpoint must be active (agent didn't archive it).
    if not op.active:
        failures.append(
            "stock.warehouse.orderpoint.active is False — agent archived "
            "the newly created rule instead of leaving it active"
        )

    # 2. Min / Max quantities
    if abs((op.product_min_qty or 0.0) - EXPECTED_MIN) > 1e-6:
        failures.append(
            f"stock.warehouse.orderpoint.product_min_qty is "
            f"{op.product_min_qty}, expected {EXPECTED_MIN} — agent may "
            f"have typed the value into the wrong numeric cell (e.g. "
            f"qty_to_order or qty_forecast) or left the default 0.0"
        )
    if abs((op.product_max_qty or 0.0) - EXPECTED_MAX) > 1e-6:
        failures.append(
            f"stock.warehouse.orderpoint.product_max_qty is "
            f"{op.product_max_qty}, expected {EXPECTED_MAX} — agent may "
            f"have typed the value into the wrong numeric cell or left "
            f"the default 0.0"
        )

    # 3. Location must be the WH/Stock internal location
    location = _find_stock_location(env)
    if not location:
        failures.append("Cannot find WH/Stock location for verification")
    elif op.location_id.id != location.id:
        failures.append(
            f"stock.warehouse.orderpoint.location_id is "
            f"'{op.location_id.complete_name}', expected "
            f"'{location.complete_name}' (WH/Stock) — agent may have "
            f"changed the default Location"
        )

    # Product linkage sanity
    if op.product_id.id != product.id:
        failures.append(
            f"stock.warehouse.orderpoint.product_id is "
            f"'{op.product_id.display_name}', expected '{PRODUCT_NAME}' — "
            f"agent likely replaced the default product before saving"
        )

    return failures
