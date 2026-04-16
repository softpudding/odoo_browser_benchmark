"""Postcondition checks for stock.update_reorder_rule."""


TARGET_PRODUCT = "Steel Bracket 12\""
DISTRACTOR_PRODUCT = "Copper Wire 100m"
EXPECTED_MIN_QTY = 50.0
EXPECTED_MAX_QTY = 200.0
ORIGINAL_DISTRACTOR_MIN = 20.0
ORIGINAL_DISTRACTOR_MAX = 100.0


def check(env):
    failures = []

    target_product = env["product.product"].search(
        [("name", "=", TARGET_PRODUCT)], limit=1
    )
    if not target_product:
        return [f"Product '{TARGET_PRODUCT}' not found"]

    target_rule = env["stock.warehouse.orderpoint"].search(
        [("product_id", "=", target_product.id)], limit=1
    )
    if not target_rule:
        return [f"No reorder rule found for '{TARGET_PRODUCT}'"]

    if target_rule.product_min_qty != EXPECTED_MIN_QTY:
        failures.append(
            f"Min Qty is {target_rule.product_min_qty}, expected {EXPECTED_MIN_QTY}"
        )
    if target_rule.product_max_qty != EXPECTED_MAX_QTY:
        failures.append(
            f"Max Qty is {target_rule.product_max_qty}, expected {EXPECTED_MAX_QTY}"
        )

    # Distractor rule must not be changed
    distractor_product = env["product.product"].search(
        [("name", "=", DISTRACTOR_PRODUCT)], limit=1
    )
    if distractor_product:
        distractor_rule = env["stock.warehouse.orderpoint"].search(
            [("product_id", "=", distractor_product.id)], limit=1
        )
        if distractor_rule:
            if distractor_rule.product_min_qty != ORIGINAL_DISTRACTOR_MIN:
                failures.append(
                    f"Distractor rule min qty changed to {distractor_rule.product_min_qty}, "
                    f"should remain {ORIGINAL_DISTRACTOR_MIN}"
                )
            if distractor_rule.product_max_qty != ORIGINAL_DISTRACTOR_MAX:
                failures.append(
                    f"Distractor rule max qty changed to {distractor_rule.product_max_qty}, "
                    f"should remain {ORIGINAL_DISTRACTOR_MAX}"
                )

    return failures
