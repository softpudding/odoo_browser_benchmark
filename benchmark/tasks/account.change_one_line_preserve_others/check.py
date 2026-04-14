"""Postcondition checks for account.change_one_line_preserve_others.

The diff engine only captures changes, so unchanged lines can't be validated
there. This check verifies:
1. The invoice is posted (net state: posted -> draft -> posted)
2. The three untouched lines retain their exact original values
"""


def check(env):
    failures = []

    invoice = env["account.move"].search([
        ("ref", "=", "SURG-EDIT-01"),
        ("move_type", "=", "out_invoice"),
    ], limit=1)

    if not invoice:
        return ["Invoice SURG-EDIT-01 not found"]

    # Must be posted
    if invoice.state != "posted":
        failures.append(
            f"Invoice state is '{invoice.state}', expected 'posted'"
        )

    # Check each line
    expected_lines = {
        "Strategy Report":  {"quantity": 1.0, "price_unit": 3000.0, "discount": 0.0},
        "Market Analysis":  {"quantity": 2.0, "price_unit": 1500.0, "discount": 10.0},
        "Risk Assessment":  {"quantity": 2.0, "price_unit": 2200.0, "discount": 5.0},
        "Compliance Audit": {"quantity": 3.0, "price_unit": 800.0,  "discount": 0.0},
    }

    for line in invoice.invoice_line_ids.filtered(lambda l: l.display_type == "product"):
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
