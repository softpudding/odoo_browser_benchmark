"""Postcondition checks for purchase.cancel_reissue_wrong_vendor.

Validates the original PO is cancelled, and a new confirmed PO
exists for Pinnacle Parts with exact line data.
"""


def check(env):
    failures = []

    # Original PO must still exist and be cancelled
    atlas = env["res.partner"].search([("name", "=", "Atlas Industrial")], limit=1)
    if not atlas:
        return ["Vendor 'Atlas Industrial' not found"]

    old_po = env["purchase.order"].search([
        ("partner_id", "=", atlas.id),
        ("origin", "=", "VENDOR-FIX-01"),
    ], limit=1)
    if not old_po:
        failures.append("Original PO (Atlas Industrial, VENDOR-FIX-01) not found — must not be deleted")
    elif old_po.state != "cancel":
        failures.append(f"Original PO state is '{old_po.state}', expected 'cancel'")

    # New PO must exist for Pinnacle Parts and be confirmed
    pinnacle = env["res.partner"].search([("name", "=", "Pinnacle Parts")], limit=1)
    if not pinnacle:
        return failures + ["Vendor 'Pinnacle Parts' not found"]

    new_po = env["purchase.order"].search([
        ("partner_id", "=", pinnacle.id),
        ("state", "=", "purchase"),
    ], limit=1)
    if not new_po:
        failures.append("No confirmed PO found for Pinnacle Parts")
        return failures

    # Check lines on the new PO
    expected_lines = {
        "Hydraulic Pump":  {"product_qty": 5.0,  "price_unit": 340.0},
        "Pressure Gauge":  {"product_qty": 10.0, "price_unit": 85.0},
    }

    if len(new_po.order_line) != 2:
        failures.append(f"New PO has {len(new_po.order_line)} lines, expected 2")

    for line in new_po.order_line:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected line on new PO: {name}")
            continue
        exp = expected_lines.pop(name)
        for field, val in exp.items():
            actual = getattr(line, field)
            if abs(actual - val) > 0.01:
                failures.append(f"New PO line {name}.{field}: expected {val}, got {actual}")

    for missing in expected_lines:
        failures.append(f"Missing line on new PO: {missing}")

    return failures
