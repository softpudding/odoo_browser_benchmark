"""Checks for purchase_stock.receive_partial_scrap_damaged_units."""

ORIGIN = "SCRAP-PO-07"
VENDOR_NAME = "Bench Harbor Supply"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", ORIGIN),
    ], order="id desc", limit=1)
    if not po:
        return [f"PO '{ORIGIN}' not found"]

    if po.receipt_status != "full":
        failures.append(f"PO receipt_status is '{po.receipt_status}', expected 'full'")

    if len(po.picking_ids) != 2:
        failures.append(f"Expected exactly 2 receipts on the PO, found {len(po.picking_ids)}")
    done_pickings = po.picking_ids.filtered(lambda p: p.state == "done")
    if len(done_pickings) != 2:
        failures.append(f"Expected 2 done receipts, found {len(done_pickings)}")

    expected_lines = {
        "Bench Control Valve": {"product_qty": 6.0, "qty_received": 6.0, "price_unit": 48.0},
        "Bench Filter Cartridge": {"product_qty": 10.0, "qty_received": 10.0, "price_unit": 12.0},
    }
    for line in po.order_line:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected PO line '{name}'")
            continue
        expected = expected_lines.pop(name)
        for field, value in expected.items():
            actual = getattr(line, field)
            if abs(actual - value) > 0.01:
                failures.append(f"PO line {name}.{field} is {actual}, expected {value}")
    for missing in expected_lines:
        failures.append(f"Missing PO line '{missing}'")

    root_receipt = po.picking_ids.filtered(lambda p: not p.backorder_id)[:1]
    if not root_receipt:
        failures.append("Could not identify the first receipt on the PO")
        return failures

    scraps = env["stock.scrap"].with_context(active_test=False).search([
        ("picking_id", "=", root_receipt.id),
    ])
    if len(scraps) != 1:
        failures.append(f"Expected exactly 1 scrap linked to the first receipt, found {len(scraps)}")
    else:
        scrap = scraps[0]
        if scrap.state != "done":
            failures.append(f"Scrap state is '{scrap.state}', expected 'done'")
        if scrap.product_id.name != "Bench Filter Cartridge":
            failures.append(
                f"Scrap product is '{scrap.product_id.name}', expected 'Bench Filter Cartridge'"
            )
        if abs(scrap.scrap_qty - 1.0) > 0.01:
            failures.append(f"Scrap quantity is {scrap.scrap_qty}, expected 1.0")

    return failures
