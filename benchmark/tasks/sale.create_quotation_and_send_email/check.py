"""Postcondition checks for sale.create_quotation_and_send_email.

Validates the quotation was created with exact lines and sent by email.
"""


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", "Riverton Supply Co.")], limit=1)
    if not partner:
        return ["Customer 'Riverton Supply Co.' not found"]

    orders = env["sale.order"].search([
        ("partner_id", "=", partner.id),
    ])

    if len(orders) == 0:
        return ["No quotation found for Riverton Supply Co."]
    if len(orders) > 1:
        failures.append(f"Expected 1 quotation, found {len(orders)}")

    so = orders[0]

    # Must be in "sent" state
    if so.state != "sent":
        failures.append(f"Quotation state is '{so.state}', expected 'sent'")

    # Check expiration date
    if str(so.validity_date) != "2026-05-15":
        failures.append(
            f"Expiration date is '{so.validity_date}', expected '2026-05-15'"
        )

    # Check lines
    expected_lines = {
        "Industrial Fan":       {"product_uom_qty": 6.0,  "price_unit": 185.0},
        "Air Filter Cartridge": {"product_uom_qty": 12.0, "price_unit": 45.0},
    }

    product_lines = so.order_line.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
        and l.product_id
    )

    if len(product_lines) != 2:
        failures.append(
            f"Expected 2 product lines, found {len(product_lines)} "
            f"(products: {[l.product_id.name for l in product_lines]})"
        )

    for line in product_lines:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected product line: {name}")
            continue
        exp = expected_lines.pop(name)
        for field, val in exp.items():
            actual = getattr(line, field)
            if abs(actual - val) > 0.01:
                failures.append(f"{name}.{field}: expected {val}, got {actual}")

    for missing in expected_lines:
        failures.append(f"Missing product line: {missing}")

    return failures
