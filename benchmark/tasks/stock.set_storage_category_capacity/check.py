"""Postcondition checks for stock.set_storage_category_capacity.

Verifies:
- A stock.storage.category named 'Bench Small Bin' exists with
  max_weight=50.0 and allow_new_product='same'.
- The internal location 'WH/Stock/Bench Small Bin Area' has its
  storage_category_id pointing to the 'Bench Small Bin' category.
"""


CATEGORY_NAME = "Bench Small Bin"
LOCATION_COMPLETE_NAME = "WH/Stock/Bench Small Bin Area"


def check(env):
    failures = []

    cats = env["stock.storage.category"].search(
        [("name", "=", CATEGORY_NAME)]
    )
    if not cats:
        return [f"Storage category '{CATEGORY_NAME}' not found"]
    if len(cats) > 1:
        failures.append(
            f"Expected exactly one storage category named "
            f"'{CATEGORY_NAME}', found {len(cats)}"
        )
    cat = cats[:1]

    if abs(cat.max_weight - 50.0) > 1e-4:
        failures.append(
            f"Storage category max_weight is {cat.max_weight}, expected 50.0"
        )
    if cat.allow_new_product != "same":
        failures.append(
            f"Storage category allow_new_product is "
            f"'{cat.allow_new_product}', expected 'same'"
        )

    loc = env["stock.location"].search(
        [("complete_name", "=", LOCATION_COMPLETE_NAME)], limit=1
    )
    if not loc:
        failures.append(
            f"Sub-location '{LOCATION_COMPLETE_NAME}' not found"
        )
        return failures

    if not loc.storage_category_id:
        failures.append(
            f"Sub-location '{LOCATION_COMPLETE_NAME}' has no "
            f"storage_category_id assigned"
        )
    elif loc.storage_category_id.id != cat.id:
        failures.append(
            f"Sub-location '{LOCATION_COMPLETE_NAME}' has "
            f"storage_category_id='{loc.storage_category_id.name}', "
            f"expected '{CATEGORY_NAME}'"
        )

    return failures
