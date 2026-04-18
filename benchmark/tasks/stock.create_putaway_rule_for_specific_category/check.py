"""Postcondition checks for stock.create_putaway_rule_for_specific_category."""

CATEGORY_NAME = "Bench Cold Items"
DISTRACTOR_PRODUCT = "Bench Frozen Salmon"
EXPECTED_LOC_IN = "WH/Stock"
EXPECTED_LOC_OUT = "WH/Stock/Refrigerator"


def check(env):
    failures = []

    cat = env["product.category"].search(
        [("name", "=", CATEGORY_NAME)], limit=1
    )
    if not cat:
        return [f"Product category '{CATEGORY_NAME}' not found (seed issue)"]

    rules = env["stock.putaway.rule"].search([
        ("category_id", "=", cat.id),
    ])
    if not rules:
        return [
            f"No stock.putaway.rule found for category '{CATEGORY_NAME}'"
        ]
    if len(rules) > 1:
        failures.append(
            f"Expected exactly 1 putaway rule for category "
            f"'{CATEGORY_NAME}', found {len(rules)}"
        )

    rule = rules[0]

    if rule.product_id:
        failures.append(
            f"Rule must be CATEGORY-level: product_id should be empty, "
            f"but is set to '{rule.product_id.display_name}'"
        )

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

    # The distractor product must not have its own product-level rule.
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
                f"product-level putaway rule, but {len(dist_rules)} were found"
            )

    # Guard against stray empty/placeholder putaway rules with no product
    # and no category.
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
