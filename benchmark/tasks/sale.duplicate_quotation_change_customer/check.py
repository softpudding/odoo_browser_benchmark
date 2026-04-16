"""Postcondition checks for sale.duplicate_quotation_change_customer.

Validates:
1. Original quotation BENCH-DUP-01 still exists and is unchanged
   (same customer Azure Interior, still draft, still has two lines).
2. A NEW draft quotation exists with Customer Reference SV-DUP-2026
   and customer Summit Ventures.
3. The duplicate carries the same two product lines with identical
   products, quantities, and prices.
4. No extra or missing records in the BENCH-DUP-01 / SV-DUP-2026 set.
"""


def check(env):
    failures = []

    azure = env["res.partner"].search(
        [("name", "=", "Azure Interior")], limit=1
    )
    summit = env["res.partner"].search(
        [("name", "=", "Summit Ventures")], limit=1
    )
    if not azure or not summit:
        return ["Seed partners Azure Interior / Summit Ventures not found"]

    # --- Original must still exist and be unchanged ---
    original = env["sale.order"].search(
        [("client_order_ref", "=", "BENCH-DUP-01")], limit=1
    )
    if not original:
        failures.append("Original quotation 'BENCH-DUP-01' is missing")
    else:
        if original.partner_id.id != azure.id:
            failures.append(
                f"Original customer is '{original.partner_id.display_name}', "
                "expected 'Azure Interior'"
            )
        if original.state != "draft":
            failures.append(
                f"Original state is '{original.state}', expected 'draft'"
            )
        if len(original.order_line) != 2:
            failures.append(
                f"Original has {len(original.order_line)} lines, expected 2"
            )

    # --- Duplicate must exist for Summit Ventures ---
    dup = env["sale.order"].search(
        [("client_order_ref", "=", "SV-DUP-2026")], limit=1
    )
    if not dup:
        return failures + [
            "Duplicated quotation with reference 'SV-DUP-2026' not found"
        ]

    if dup.partner_id.id != summit.id:
        failures.append(
            f"Duplicate customer is '{dup.partner_id.display_name}', "
            "expected 'Summit Ventures'"
        )
    if dup.state != "draft":
        failures.append(
            f"Duplicate state is '{dup.state}', expected 'draft'"
        )

    # --- Line integrity on the duplicate ---
    lines = dup.order_line
    if len(lines) != 2:
        failures.append(
            f"Duplicate has {len(lines)} lines, expected 2"
        )
        return failures

    ergo = lines.filtered(lambda l: l.product_id.name == "Ergo Chair")
    lamp = lines.filtered(lambda l: l.product_id.name == "Desk Lamp")
    if not ergo:
        failures.append("Duplicate is missing the Ergo Chair line")
    else:
        if ergo.product_uom_qty != 3:
            failures.append(
                f"Duplicate Ergo Chair qty is {ergo.product_uom_qty}, expected 3"
            )
        if ergo.price_unit != 260.0:
            failures.append(
                f"Duplicate Ergo Chair price is {ergo.price_unit}, expected 260.0"
            )
    if not lamp:
        failures.append("Duplicate is missing the Desk Lamp line")
    else:
        if lamp.product_uom_qty != 4:
            failures.append(
                f"Duplicate Desk Lamp qty is {lamp.product_uom_qty}, expected 4"
            )
        if lamp.price_unit != 45.0:
            failures.append(
                f"Duplicate Desk Lamp price is {lamp.price_unit}, expected 45.0"
            )

    # --- No extra records using either reference ---
    extras = env["sale.order"].search([
        ("client_order_ref", "in", ["BENCH-DUP-01", "SV-DUP-2026"]),
    ])
    if len(extras) != 2:
        failures.append(
            f"Expected exactly 2 orders across {{BENCH-DUP-01, SV-DUP-2026}}, "
            f"found {len(extras)}"
        )

    return failures
