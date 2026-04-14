"""Postcondition checks for sale.confirm_order_within_credit_limit.

Validates that unchanged lines remain intact and total is within credit limit.
"""


def check(env):
    failures = []

    so = env["sale.order"].search([
        ("client_order_ref", "=", "CREDIT-CHECK-01"),
    ], limit=1)

    if not so:
        return ["Order CREDIT-CHECK-01 not found"]

    # Must be confirmed
    if so.state != "sale":
        failures.append(f"Order state is '{so.state}', expected 'sale'")

    # Total must be within credit limit
    partner = so.partner_id
    if partner.credit_limit and so.amount_untaxed > partner.credit_limit:
        failures.append(
            f"Order total {so.amount_untaxed} exceeds credit limit {partner.credit_limit}"
        )

    # Exact total check
    if abs(so.amount_untaxed - 4900.0) > 0.01:
        failures.append(
            f"Order untaxed total is {so.amount_untaxed}, expected 4900.0"
        )

    # Check all lines (including discount = 0 to catch unintended changes)
    expected_lines = {
        "Server Rack":     {"product_uom_qty": 2.0, "price_unit": 1200.0, "discount": 0.0},
        "Network Switch":  {"product_uom_qty": 5.0, "price_unit": 400.0, "discount": 0.0},
        "Patch Cable Kit": {"product_uom_qty": 10.0, "price_unit": 50.0, "discount": 0.0},
    }

    for line in so.order_line:
        product_name = line.product_id.name
        if product_name not in expected_lines:
            failures.append(f"Unexpected product line: {product_name}")
            continue

        expected = expected_lines.pop(product_name)
        for field, expected_val in expected.items():
            actual = getattr(line, field)
            if abs(actual - expected_val) > 0.01:
                failures.append(
                    f"{product_name}.{field}: expected {expected_val}, got {actual}"
                )

    for missing in expected_lines:
        failures.append(f"Missing product line: {missing}")

    return failures
