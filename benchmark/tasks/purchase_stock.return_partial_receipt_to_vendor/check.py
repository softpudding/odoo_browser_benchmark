"""Postcondition checks for purchase_stock.return_partial_receipt_to_vendor."""


TARGET_ORIGIN = "RET-PO-07"
DISTRACTOR_ORIGIN = "RET-PO-08"


def check(env):
    failures = []

    target = env["purchase.order"].search([("origin", "=", TARGET_ORIGIN)], limit=1)
    distractor = env["purchase.order"].search([("origin", "=", DISTRACTOR_ORIGIN)], limit=1)

    if not target:
        return [f"Target purchase order {TARGET_ORIGIN!r} not found"]
    if not distractor:
        return [f"Distractor purchase order {DISTRACTOR_ORIGIN!r} not found"]

    expected_qty = {
        "Servo Motor X2": 4.0,
        "Sensor Harness Pro": 4.0,
        "Panel Bracket 90": 4.0,
    }
    for line in target.order_line:
        exp = expected_qty.get(line.product_id.name)
        if exp is None:
            failures.append(f"Unexpected target PO line {line.product_id.name!r}")
            continue
        if abs(float(line.qty_received or 0.0) - exp) > 0.001:
            failures.append(
                f"{line.product_id.name} received qty is {line.qty_received}, expected {exp}"
            )

    return_pickings = target.picking_ids.filtered(lambda p: p.return_id)
    if len(return_pickings) != 1:
        failures.append(f"Expected exactly 1 return picking, found {len(return_pickings)}")
    else:
        picking = return_pickings[0]
        if picking.state != "done":
            failures.append(f"Return picking state is {picking.state!r}, expected 'done'")
        expected_moves = {
            "Servo Motor X2": 2.0,
            "Panel Bracket 90": 1.0,
        }
        actual_names = set()
        for move in picking.move_ids.filtered(lambda m: m.state != "cancel"):
            actual_names.add(move.product_id.name)
            exp = expected_moves.get(move.product_id.name)
            if exp is None:
                failures.append(f"Unexpected product returned: {move.product_id.name}")
                continue
            if abs(float(move.quantity or 0.0) - exp) > 0.001:
                failures.append(
                    f"Return move {move.product_id.name} quantity is {move.quantity}, expected {exp}"
                )
        missing = set(expected_moves) - actual_names
        if missing:
            failures.append(f"Missing expected return move(s): {sorted(missing)}")
        if "Sensor Harness Pro" in actual_names:
            failures.append("Sensor Harness Pro was returned but should have remained at 0")

    distractor_qty = {
        "Servo Motor X2": 3.0,
        "Sensor Harness Pro": 2.0,
    }
    for line in distractor.order_line:
        exp = distractor_qty.get(line.product_id.name)
        if exp is None:
            continue
        if abs(float(line.qty_received or 0.0) - exp) > 0.001:
            failures.append(
                f"Distractor line {line.product_id.name} received qty changed to {line.qty_received}"
            )

    if distractor.picking_ids.filtered(lambda p: p.return_id):
        failures.append("Distractor purchase order gained a return picking")

    return failures
