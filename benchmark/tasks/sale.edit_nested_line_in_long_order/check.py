"""Postcondition checks for sale.edit_nested_line_in_long_order.

Validates that the 19 untouched lines retain their original values
and that no lines were added or removed.
"""

ORIGINAL_LINES = {
    "Executive Desk":          {"product_uom_qty": 2.0,  "price_unit": 890.0,  "discount": 0.0},
    "Mesh Office Chair":       {"product_uom_qty": 6.0,  "price_unit": 450.0,  "discount": 5.0},
    "Filing Cabinet 3-Drawer": {"product_uom_qty": 4.0,  "price_unit": 220.0,  "discount": 0.0},
    "Ergonomic Keyboard":      {"product_uom_qty": 10.0, "price_unit": 75.0,   "discount": 0.0},
    "Monitor Stand":           {"product_uom_qty": 8.0,  "price_unit": 65.0,   "discount": 0.0},
    "Whiteboard 120x90":       {"product_uom_qty": 3.0,  "price_unit": 180.0,  "discount": 0.0},
    "Desk Lamp LED":           {"product_uom_qty": 12.0, "price_unit": 55.0,   "discount": 0.0},
    "Ergonomic Mouse Pad":     {"product_uom_qty": 15.0, "price_unit": 25.0,   "discount": 0.0},
    "Cable Management Kit":    {"product_uom_qty": 20.0, "price_unit": 35.0,   "discount": 0.0},
    "Privacy Screen Filter":   {"product_uom_qty": 6.0,  "price_unit": 45.0,   "discount": 0.0},
    "Acoustic Panel Set":      {"product_uom_qty": 4.0,  "price_unit": 310.0,  "discount": 10.0},
    "Standing Desk Converter": {"product_uom_qty": 3.0,  "price_unit": 380.0,  "discount": 0.0},
    "Bookshelf Unit":          {"product_uom_qty": 2.0,  "price_unit": 260.0,  "discount": 0.0},
    "Visitor Chair":           {"product_uom_qty": 8.0,  "price_unit": 175.0,  "discount": 0.0},
    "Desk Organizer":          {"product_uom_qty": 10.0, "price_unit": 40.0,   "discount": 0.0},
    "Ergonomic Footrest":      {"product_uom_qty": 12.0, "price_unit": 95.0,   "discount": 8.0},
    "Conference Table":        {"product_uom_qty": 1.0,  "price_unit": 1200.0, "discount": 0.0},
    "Projector Mount":         {"product_uom_qty": 4.0,  "price_unit": 85.0,   "discount": 0.0},
    "Coat Rack":               {"product_uom_qty": 3.0,  "price_unit": 120.0,  "discount": 0.0},
    "Reception Desk":          {"product_uom_qty": 1.0,  "price_unit": 1500.0, "discount": 5.0},
}


def check(env):
    failures = []

    so = env["sale.order"].search([
        ("client_order_ref", "=", "LONG-ORDER-01"),
    ], limit=1)

    if not so:
        return ["Order LONG-ORDER-01 not found"]

    if so.state != "sale":
        failures.append(f"Order state is '{so.state}', expected 'sale'")

    if len(so.order_line) != 20:
        failures.append(f"Expected 20 lines, found {len(so.order_line)}")

    expected = dict(ORIGINAL_LINES)
    for line in so.order_line:
        product_name = line.product_id.name
        if product_name not in expected:
            failures.append(f"Unexpected product line: {product_name}")
            continue

        exp = expected.pop(product_name)
        for field, expected_val in exp.items():
            actual = getattr(line, field)
            if abs(actual - expected_val) > 0.01:
                failures.append(
                    f"{product_name}.{field}: expected {expected_val}, got {actual}"
                )

    for missing in expected:
        failures.append(f"Missing product line: {missing}")

    return failures
