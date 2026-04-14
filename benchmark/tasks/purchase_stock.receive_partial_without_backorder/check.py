"""Postcondition checks for purchase_stock.receive_partial_without_backorder."""


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", "North Coast Components")], limit=1)
    if not vendor:
        return ["Vendor 'North Coast Components' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "NOBACK-04"),
    ], limit=1)
    if not po:
        return ["PO with origin NOBACK-04 not found"]

    if po.receipt_status != "full":
        failures.append(f"PO receipt_status is {po.receipt_status!r}, expected 'full'")

    if len(po.picking_ids) != 1:
        failures.append(f"Expected exactly 1 receipt on the PO, found {len(po.picking_ids)}")
    elif po.picking_ids[0].state != "done":
        failures.append(
            f"Receipt state is {po.picking_ids[0].state!r}, expected 'done'"
        )

    expected_lines = {
        "Servo Motor": {"product_qty": 8.0, "qty_received": 6.0, "price_unit": 230.0},
        "Sensor Harness": {"product_qty": 12.0, "qty_received": 9.0, "price_unit": 18.0},
    }

    for line in po.order_line:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected PO line: {name}")
            continue
        expected = expected_lines.pop(name)
        for field, value in expected.items():
            actual = getattr(line, field)
            if abs(actual - value) > 0.01:
                failures.append(f"PO line {name}.{field}: expected {value}, got {actual}")

    for missing in expected_lines:
        failures.append(f"Missing PO line: {missing}")

    return failures
