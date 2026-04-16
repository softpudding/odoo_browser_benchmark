"""Postcondition checks for stock.update_product_internal_reference.

Validates:
1. Product "Steel Bracket 12" exists
2. Internal Reference (default_code) is "SB-12-BENCH"
"""

PRODUCT_NAME = "Steel Bracket 12"


def check(env):
    failures = []

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    expected_ref = "SB-12-BENCH"
    actual_ref = product.default_code or ""
    if actual_ref != expected_ref:
        failures.append(f"Internal Reference is '{actual_ref}', expected '{expected_ref}'")

    return failures