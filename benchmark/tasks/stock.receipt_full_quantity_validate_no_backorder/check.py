"""Postcondition checks for stock.receipt_full_quantity_validate_no_backorder.

Validates:
  1. Original incoming picking (name=WH/IN/BENCH-FULL) is in state 'done'
     with a single Bench Recv Item move whose quantity == 10.
  2. NO backorder stock.picking exists with backorder_id == original.id
     (qty matched demand exactly, so no backorder should ever be created).
  3. Exactly one incoming picking exists with that name (no duplicates /
     extras for the vendor).
  4. On-hand at WH/Stock for Bench Recv Item == 10 (goods put away).
"""

PICKING_NAME = "WH/IN/BENCH-FULL"
VENDOR_NAME = "Bench Vendor"
PRODUCT_NAME = "Bench Recv Item"
DONE_QTY = 10.0
EXPECTED_ON_HAND = 10.0


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    # ------------------------------------------------------------------
    # 1. Original incoming picking (identified by pinned name)
    # ------------------------------------------------------------------
    originals = env["stock.picking"].search([
        ("name", "=", PICKING_NAME),
        ("picking_type_id.code", "=", "incoming"),
    ])
    if not originals:
        return failures + [
            f"Incoming receipt '{PICKING_NAME}' not found"
        ]
    if len(originals) > 1:
        failures.append(
            f"Expected exactly 1 receipt named '{PICKING_NAME}', "
            f"found {len(originals)}"
        )
    original = originals[:1]

    if original.state != "done":
        failures.append(
            f"Receipt '{PICKING_NAME}' state is '{original.state}', "
            f"expected 'done' — did the agent click Validate?"
        )

    moves = original.move_ids.filtered(
        lambda m: m.product_id.id == product.id and not m.scrap_id
    )
    if len(moves) != 1:
        failures.append(
            f"Receipt has {len(moves)} Bench Recv Item moves, expected 1"
        )
    else:
        mv = moves[0]
        if abs((mv.quantity or 0.0) - DONE_QTY) > 1e-6:
            failures.append(
                f"Receipt Bench Recv Item Quantity (Done) is "
                f"{mv.quantity}, expected {DONE_QTY} — Done quantity "
                f"should remain unchanged (agent must not edit the "
                f"Done cell)"
            )

    # ------------------------------------------------------------------
    # 2. NO backorder picking should have been created
    # ------------------------------------------------------------------
    backorders = env["stock.picking"].search([
        ("backorder_id", "=", original.id),
    ])
    if backorders:
        failures.append(
            f"Found {len(backorders)} backorder picking(s) for "
            f"'{PICKING_NAME}' ({backorders.mapped('name')}) — since "
            f"Done (10) matched Demand (10), no backorder should ever "
            f"have been created"
        )

    # ------------------------------------------------------------------
    # 3. Guard against extra incoming pickings for this vendor
    # ------------------------------------------------------------------
    all_pickings_vnd = env["stock.picking"].search([
        ("partner_id", "=", vendor.id),
        ("picking_type_id.code", "=", "incoming"),
    ])
    non_cancel = all_pickings_vnd.filtered(lambda p: p.state != "cancel")
    if len(non_cancel) > 1:
        failures.append(
            f"Found {len(non_cancel)} non-cancelled incoming pickings "
            f"for '{VENDOR_NAME}', expected exactly 1: "
            f"{non_cancel.mapped('name')}"
        )

    # ------------------------------------------------------------------
    # 4. Stock on-hand at WH/Stock should be 10 (goods received)
    # ------------------------------------------------------------------
    wh = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    if wh:
        stock_location = wh.lot_stock_id
        quants = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", stock_location.id),
        ])
        on_hand = sum(q.quantity for q in quants)
        if abs(on_hand - EXPECTED_ON_HAND) > 1e-6:
            failures.append(
                f"On-hand of '{PRODUCT_NAME}' at WH/Stock is {on_hand}, "
                f"expected {EXPECTED_ON_HAND} (a validated receipt for "
                f"10 units should land a stock.quant of 10 at WH/Stock)"
            )

    return failures
