"""Postcondition checks for purchase_stock.receive_and_complete_backorder.

Validates both receipts are Done with correct quantities,
and the PO is fully received.
"""


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", "Stellar Supplies")], limit=1)
    if not vendor:
        return ["Vendor 'Stellar Supplies' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "BENCH-PARTIAL"),
    ], limit=1)
    if not po:
        return ["PO with origin BENCH-PARTIAL not found"]

    # PO must be fully received
    if po.receipt_status != "full":
        failures.append(
            f"PO receipt_status is '{po.receipt_status}', expected 'full'"
        )

    # Must have exactly 2 done receipts
    done_pickings = po.picking_ids.filtered(lambda p: p.state == "done")
    if len(done_pickings) != 2:
        failures.append(
            f"Expected 2 done receipts, found {len(done_pickings)} "
            f"(total pickings: {len(po.picking_ids)}, "
            f"states: {[p.state for p in po.picking_ids]})"
        )

    # PO lines must be unchanged
    expected_lines = {
        "Copper Wire Spool": {"product_qty": 10.0, "price_unit": 45.0},
        "Steel Bracket":     {"product_qty": 20.0, "price_unit": 12.0},
    }
    for line in po.order_line:
        name = line.product_id.name
        if name not in expected_lines:
            failures.append(f"Unexpected PO line: {name}")
            continue
        exp = expected_lines.pop(name)
        for field, val in exp.items():
            actual = getattr(line, field)
            if abs(actual - val) > 0.01:
                failures.append(f"PO line {name}.{field}: expected {val}, got {actual}")

    for missing in expected_lines:
        failures.append(f"Missing PO line: {missing}")

    return failures
