"""Postcondition checks for stock.create_putaway_rule."""

TARGET_PRODUCT = "Storage Box Echo"
DISTRACTOR_PRODUCT = "Storage Box Foxtrot"
EXPECTED_LOC_IN = "WH/Stock"
EXPECTED_LOC_OUT = "WH/Stock/Shelf A1"


def check(env):
    failures = []

    target_product = env["product.product"].search(
        [("name", "=", TARGET_PRODUCT)], limit=1
    )
    if not target_product:
        return [f"Product '{TARGET_PRODUCT}' not found (seed issue)"]

    rules = env["stock.putaway.rule"].search([
        ("product_id", "=", target_product.id),
    ])
    if not rules:
        return [
            f"No stock.putaway.rule found for product '{TARGET_PRODUCT}'"
        ]
    if len(rules) > 1:
        failures.append(
            f"Expected exactly 1 putaway rule for '{TARGET_PRODUCT}', "
            f"found {len(rules)}"
        )

    rule = rules[0]

    if rule.location_in_id.complete_name != EXPECTED_LOC_IN:
        failures.append(
            f"location_in_id is '{rule.location_in_id.complete_name}', "
            f"expected '{EXPECTED_LOC_IN}'"
        )
    if rule.location_out_id.complete_name != EXPECTED_LOC_OUT:
        failures.append(
            f"location_out_id is '{rule.location_out_id.complete_name}', "
            f"expected '{EXPECTED_LOC_OUT}'"
        )

    # The distractor product must not have a rule.
    distractor = env["product.product"].search(
        [("name", "=", DISTRACTOR_PRODUCT)], limit=1
    )
    if distractor:
        dist_rules = env["stock.putaway.rule"].search([
            ("product_id", "=", distractor.id),
        ])
        if dist_rules:
            failures.append(
                f"Distractor product '{DISTRACTOR_PRODUCT}' should have no "
                f"putaway rule, but {len(dist_rules)} were found"
            )

    # Guard against stray empty/placeholder putaway rules with no product
    # and no category that may be left behind by an agent that clicked
    # Save before filling the many2ones.
    empty = env["stock.putaway.rule"].search([
        ("product_id", "=", False),
        ("category_id", "=", False),
    ])
    if empty:
        failures.append(
            f"Found {len(empty)} empty putaway rule(s) with no product and "
            f"no category (agent likely saved a blank row)"
        )

    return failures
