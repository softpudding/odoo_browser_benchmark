"""Postcondition checks for stock.set_putaway_rule_default_location."""

PRODUCT_NAME = "Bench Putaway Item"
EXPECTED_LOC_IN = "WH/Stock"
EXPECTED_LOC_OUT = "WH/Stock/Shelf B"


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found (seed issue)"]

    # Product integrity sanity
    if product.type != "consu":
        failures.append(
            f"Product type is '{product.type}', expected 'consu' — "
            f"agent may have edited the product itself"
        )
    if not product.is_storable:
        failures.append(
            "Product is_storable is False, expected True — agent may "
            "have edited the product storable flag"
        )

    rules = env["stock.putaway.rule"].search(
        [("product_id", "=", product.id)]
    )
    if not rules:
        return failures + [
            f"No stock.putaway.rule found with product_id='{PRODUCT_NAME}' — "
            f"agent never created the putaway rule"
        ]
    if len(rules) > 1:
        failures.append(
            f"Expected exactly 1 putaway rule for product "
            f"'{PRODUCT_NAME}', found {len(rules)}"
        )

    rule = rules[0]

    # Rule must be product-based, not category-based.
    if rule.category_id:
        failures.append(
            f"Rule should be product-based but has category_id="
            f"'{rule.category_id.display_name}'"
        )

    if rule.location_in_id.complete_name != EXPECTED_LOC_IN:
        failures.append(
            f"location_in_id is '{rule.location_in_id.complete_name}', "
            f"expected '{EXPECTED_LOC_IN}' — agent may have swapped "
            f"source/destination or picked the wrong location"
        )
    if rule.location_out_id.complete_name != EXPECTED_LOC_OUT:
        failures.append(
            f"location_out_id is '{rule.location_out_id.complete_name}', "
            f"expected '{EXPECTED_LOC_OUT}' — agent may have picked the "
            f"wrong destination sublocation"
        )

    # Guard against stray empty/placeholder putaway rules (agent saved a
    # second blank row by mistake).
    empty = env["stock.putaway.rule"].search([
        ("product_id", "=", False),
        ("category_id", "=", False),
    ])
    if empty:
        failures.append(
            f"Found {len(empty)} empty putaway rule(s) with no product and "
            f"no category (agent likely saved a blank placeholder row)"
        )

    return failures
