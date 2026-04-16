"""Postcondition checks for purchase_stock.confirm_rfq_receive_full."""


TARGET_VENDOR = "Pioneer Industrial Supply"
TARGET_SOURCE = "MED-RECV-PO-01"
DISTRACTOR_SOURCE = "MED-RECV-PO-02"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", TARGET_VENDOR)], limit=1)
    if not vendor:
        return [f"Vendor '{TARGET_VENDOR}' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", TARGET_SOURCE),
    ], limit=1)
    distractor = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", DISTRACTOR_SOURCE),
    ], limit=1)
    if not po or not distractor:
        return ["Missing seeded purchase orders for confirm-receive task"]

    if po.state != "purchase":
        failures.append(f"Target PO state is {po.state!r}, expected 'purchase'")
    if po.receipt_status != "full":
        failures.append(
            f"Target PO receipt_status is {po.receipt_status!r}, expected 'full'"
        )

    if len(po.picking_ids) != 1:
        failures.append(f"Expected exactly 1 receipt, found {len(po.picking_ids)}")
    else:
        picking = po.picking_ids[0]
        if picking.state != "done":
            failures.append(f"Receipt state is {picking.state!r}, expected 'done'")

        expected_moves = {
            "Steel Cable Reel": 12.0,
            "Safety Tape Pack": 30.0,
        }
        for move in picking.move_ids:
            product_name = move.product_id.name
            if product_name not in expected_moves:
                failures.append(f"Unexpected move product {product_name!r}")
                continue
            expected_qty = expected_moves.pop(product_name)
            if abs(move.quantity - expected_qty) > 0.01:
                failures.append(
                    f"{product_name} done qty is {move.quantity}, expected {expected_qty}"
                )
        for missing_name in expected_moves:
            failures.append(f"Missing receipt move for {missing_name}")

    if distractor.state != "draft":
        failures.append(
            f"Distractor RFQ state is {distractor.state!r}, expected 'draft'"
        )
    if distractor.picking_ids:
        failures.append("Distractor RFQ unexpectedly generated a receipt")

    return failures
