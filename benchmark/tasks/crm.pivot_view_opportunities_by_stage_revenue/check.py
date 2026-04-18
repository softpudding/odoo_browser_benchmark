"""Postcondition checks for crm.pivot_view_opportunities_by_stage_revenue.

Validates that:
1. Exactly one ir.filters record named "Bench Stage Revenue Pivot" exists.
2. Its model_id is 'crm.lead'.
3. Its context contains both 'expected_revenue' and 'stage_id' substrings
   (encoding the Measures and row groupby).
"""

FAVORITE_NAME = "Bench Stage Revenue Pivot"
TARGET_MODEL = "crm.lead"


def check(env):
    failures = []

    favorites = env["ir.filters"].search([
        ("name", "=", FAVORITE_NAME),
    ])

    if not favorites:
        return [f"ir.filters favorite '{FAVORITE_NAME}' not found"]

    if len(favorites) > 1:
        failures.append(
            f"Expected exactly 1 favorite named '{FAVORITE_NAME}', "
            f"found {len(favorites)}"
        )

    fav = favorites[0]

    if fav.model_id != TARGET_MODEL:
        failures.append(
            f"Favorite model_id is '{fav.model_id}', expected '{TARGET_MODEL}'"
        )

    context_str = fav.context or ""
    if "expected_revenue" not in context_str:
        failures.append(
            f"Favorite context missing 'expected_revenue' (pivot measure). "
            f"Got: {context_str!r}"
        )
    if "stage_id" not in context_str:
        failures.append(
            f"Favorite context missing 'stage_id' (pivot row groupby). "
            f"Got: {context_str!r}"
        )

    return failures
