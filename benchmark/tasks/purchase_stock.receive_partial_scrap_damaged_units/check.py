"""Postcondition checks for purchase_stock.receive_partial_scrap_damaged_units.

Validates:
  * The receipt for PO BENCH-SCRAP-RCV-01 is in state 'done'.
  * The Bench Widget move on the receipt has quantity 8 (8 good units
    received).
  * Exactly one stock.scrap for Bench Widget in state 'done', quantity 2,
    tagged with 'Damaged'.
  * No backorder was created (PO has exactly one picking).
  * The purchase order is still in 'purchase' state with quantity 10 and
    price 5.0.
"""

VENDOR_NAME = "Bench Reliable Supplier"
PRODUCT_NAME = "Bench Widget"
PO_ORIGIN = "BENCH-SCRAP-RCV-01"
REASON_TAG = "Damaged"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if not products:
        return [f"Product '{PRODUCT_NAME}' not found"]
    product = products[0]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", PO_ORIGIN),
    ], limit=1)
    if not po:
        return [f"Purchase order with origin '{PO_ORIGIN}' not found"]

    # PO must not be cancelled and must keep its ordered quantity/price.
    if po.state == "cancel":
        failures.append(
            f"Purchase order state is 'cancel' — agent must not cancel the PO"
        )

    po_lines = po.order_line.filtered(lambda l: l.product_id.id == product.id)
    if len(po_lines) != 1:
        failures.append(
            f"Expected 1 PO line for '{PRODUCT_NAME}', found {len(po_lines)}"
        )
    else:
        line = po_lines[0]
        if abs(line.product_qty - 10.0) > 0.01:
            failures.append(
                f"PO line product_qty is {line.product_qty}, expected 10.0"
            )
        if abs(line.price_unit - 5.0) > 0.01:
            failures.append(
                f"PO line price_unit is {line.price_unit}, expected 5.0"
            )

    # Exactly one picking — no backorder.
    if len(po.picking_ids) != 1:
        failures.append(
            f"Expected exactly 1 receipt on PO (no backorder), found "
            f"{len(po.picking_ids)}: {po.picking_ids.mapped('name')}"
        )
    picking = po.picking_ids[:1]
    if picking:
        p = picking[0]
        if p.state != "done":
            failures.append(
                f"Receipt state is '{p.state}', expected 'done'"
            )
        if p.backorder_ids:
            failures.append(
                f"Receipt has backorder(s) {p.backorder_ids.mapped('name')!r} — "
                f"agent must have chosen 'No Backorder'"
            )

        # The Bench Widget move on the receipt must have quantity 8.
        main_moves = p.move_ids.filtered(
            lambda m: m.product_id.id == product.id and not m.scrap_id
        )
        if not main_moves:
            failures.append(
                f"No non-scrap stock.move found on the receipt for "
                f"'{PRODUCT_NAME}'"
            )
        else:
            total_qty = sum(main_moves.mapped("quantity"))
            if abs(total_qty - 8.0) > 0.01:
                failures.append(
                    f"Receipt move quantity for '{PRODUCT_NAME}' is "
                    f"{total_qty}, expected 8.0"
                )

    # Exactly one stock.scrap for Bench Widget, 2 units, done, tagged Damaged.
    scraps = env["stock.scrap"].search([("product_id", "=", product.id)])
    if len(scraps) == 0:
        failures.append(
            f"No stock.scrap exists for '{PRODUCT_NAME}' — agent did not scrap"
        )
        return failures
    if len(scraps) != 1:
        failures.append(
            f"Expected exactly 1 stock.scrap for '{PRODUCT_NAME}', found "
            f"{len(scraps)}"
        )
    s = scraps[0]
    if s.state != "done":
        failures.append(
            f"Scrap state is '{s.state}', expected 'done' — agent must "
            f"validate the scrap record"
        )
    if abs(s.scrap_qty - 2.0) > 0.01:
        failures.append(
            f"Scrap quantity is {s.scrap_qty}, expected 2"
        )
    tag_names = s.scrap_reason_tag_ids.mapped("name")
    if REASON_TAG not in tag_names:
        failures.append(
            f"Scrap reason tags {tag_names!r} do not include '{REASON_TAG}'"
        )
    # The scrap should be linked to the seeded picking.
    if picking and s.picking_id and s.picking_id.id != picking.id:
        failures.append(
            f"Scrap is linked to picking '{s.picking_id.name}' — expected "
            f"the PO's receipt"
        )

    return failures
