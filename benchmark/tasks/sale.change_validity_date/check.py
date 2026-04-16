"""Postcondition checks for sale.change_validity_date.

Validates that:
1. The target quotation's validity_date is changed to 2026-05-15
2. The quotation state remains 'draft'
"""


def check(env):
    failures = []

    # Find the target quotation
    so = env["sale.order"].search([
        ("client_order_ref", "=", "BENCH-VALID-01"),
    ], limit=1)

    if not so:
        return ["Quotation with reference 'BENCH-VALID-01' not found"]

    # Check validity_date
    expected_date = "2026-05-15"
    actual_date = str(so.validity_date) if so.validity_date else None
    if actual_date != expected_date:
        failures.append(
            f"validity_date is '{actual_date}', expected '{expected_date}'"
        )

    # Check state remains draft
    if so.state != "draft":
        failures.append(
            f"Quotation state is '{so.state}', expected 'draft' — "
            "the quotation must NOT be confirmed"
        )

    # Check partner is still Lakeview Partners
    if so.partner_id.name != "Lakeview Partners":
        failures.append(
            f"Customer changed to '{so.partner_id.name}', expected 'Lakeview Partners'"
        )

    return failures
