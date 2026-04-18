"""Postcondition checks for stock.create_putaway_rule_for_product.

Verifies:
- Exactly one stock.putaway.rule exists for the seeded product.
- The rule's location_in_id is WH/Stock.
- The rule's location_out_id is WH/Stock/Bench Shelf A.
- The rule is active, and location_in and location_out are distinct.
"""


PRODUCT_NAME = "Bench Putaway Product"
LOCATION_IN_COMPLETE = "WH/Stock"
LOCATION_OUT_COMPLETE = "WH/Stock/Bench Shelf A"


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    rules = env["stock.putaway.rule"].search(
        [("product_id", "=", product.id)]
    )
    if not rules:
        failures.append(
            f"No putaway rule found for product '{PRODUCT_NAME}'"
        )
        return failures

    if len(rules) > 1:
        failures.append(
            f"Expected exactly one putaway rule for '{PRODUCT_NAME}', "
            f"found {len(rules)}"
        )

    rule = rules[:1]

    if not rule.active:
        failures.append("Putaway rule is archived (active=False); expected active")

    if not rule.location_in_id or rule.location_in_id.complete_name != LOCATION_IN_COMPLETE:
        actual = (
            rule.location_in_id.complete_name
            if rule.location_in_id else "<unset>"
        )
        failures.append(
            f"Putaway rule location_in_id is '{actual}', "
            f"expected '{LOCATION_IN_COMPLETE}'"
        )

    if not rule.location_out_id or rule.location_out_id.complete_name != LOCATION_OUT_COMPLETE:
        actual = (
            rule.location_out_id.complete_name
            if rule.location_out_id else "<unset>"
        )
        failures.append(
            f"Putaway rule location_out_id is '{actual}', "
            f"expected '{LOCATION_OUT_COMPLETE}'"
        )

    # The target sub-location must still exist and remain a child of WH/Stock.
    sub = env["stock.location"].search(
        [("complete_name", "=", LOCATION_OUT_COMPLETE)], limit=1
    )
    if not sub:
        failures.append(
            f"Seeded sub-location '{LOCATION_OUT_COMPLETE}' is missing"
        )

    return failures
