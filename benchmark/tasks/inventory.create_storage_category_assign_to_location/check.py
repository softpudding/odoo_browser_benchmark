"""Postcondition checks for inventory.create_storage_category_assign_to_location."""

CATEGORY_NAME = "Cold Chain"
STOCK_COMPLETE = "WH/Stock"
EXPECTED_MAX_WEIGHT = 500.0


def check(env):
    failures = []

    # 1. Cold Chain category exists with max_weight=500
    cats = env["stock.storage.category"].search([
        ("name", "=", CATEGORY_NAME),
    ])
    if not cats:
        return [f"Storage category '{CATEGORY_NAME}' was not created"]
    if len(cats) > 1:
        failures.append(
            f"Expected exactly 1 storage category named '{CATEGORY_NAME}', "
            f"found {len(cats)}"
        )
    cat = cats[0]
    if abs(cat.max_weight - EXPECTED_MAX_WEIGHT) > 0.001:
        failures.append(
            f"Storage category '{CATEGORY_NAME}' has max_weight="
            f"{cat.max_weight}, expected {EXPECTED_MAX_WEIGHT}"
        )

    # 2. WH/Stock location has storage_category_id pointing to Cold Chain
    stock_loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if not stock_loc:
        failures.append(f"Stock location '{STOCK_COMPLETE}' not found")
    else:
        if not stock_loc.storage_category_id:
            failures.append(
                f"Location '{STOCK_COMPLETE}' has no storage_category_id set"
            )
        elif stock_loc.storage_category_id.id != cat.id:
            failures.append(
                f"Location '{STOCK_COMPLETE}' storage_category_id is "
                f"'{stock_loc.storage_category_id.name}', expected "
                f"'{CATEGORY_NAME}'"
            )

    # 3. Sanity: no capacity rules added (the prompt explicitly tells the agent
    # not to add capacity-by-product rows; max_weight goes on the category).
    if cat and cat.capacity_ids:
        failures.append(
            f"Category '{CATEGORY_NAME}' has {len(cat.capacity_ids)} capacity "
            f"rule(s); none should be created (max_weight goes on the category "
            f"itself, not in the capacity table)"
        )

    return failures
