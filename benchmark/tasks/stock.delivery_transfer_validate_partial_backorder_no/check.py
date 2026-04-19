"""Postcondition checks for stock.delivery_transfer_validate_partial_backorder_no.

Validates:
  1. Original outgoing picking (name=WH/OUT/BENCH-BACKORDER-NO) is in
     state 'done' with a single Bench Pick Item move whose quantity == 3.
  2. NO backorder stock.picking exists with backorder_id == original.id
     (the agent clicked 'No Backorder', so the 2 un-shipped units were
     dropped, not put on a new picking).
  3. Exactly one outgoing picking exists with that name (no accidental
     duplicates, no extra pickings).
  4. On-hand at WH/Stock for Bench Pick Item decreased by 3 (5 -> 2).
"""

PICKING_NAME = "WH/OUT/BENCH-BACKORDER-NO"
CUSTOMER_NAME = "Bench Ship Co"
PRODUCT_NAME = "Bench Pick Item"
DONE_QTY = 3.0
EXPECTED_ON_HAND = 2.0


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    customer = env["res.partner"].search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )
    if not customer:
        return [f"Customer '{CUSTOMER_NAME}' not found"]

    # ------------------------------------------------------------------
    # 1. Original outgoing picking (identified by pinned name)
    # ------------------------------------------------------------------
    originals = env["stock.picking"].search([
        ("name", "=", PICKING_NAME),
        ("picking_type_id.code", "=", "outgoing"),
    ])
    if not originals:
        return failures + [
            f"Original delivery '{PICKING_NAME}' not found"
        ]
    if len(originals) > 1:
        failures.append(
            f"Expected exactly 1 delivery named '{PICKING_NAME}', "
            f"found {len(originals)}"
        )
    original = originals[:1]

    if original.state != "done":
        failures.append(
            f"Delivery '{PICKING_NAME}' state is '{original.state}', "
            f"expected 'done' — did the agent click Validate and then "
            f"'No Backorder' on the dialog?"
        )

    moves = original.move_ids.filtered(
        lambda m: m.product_id.id == product.id and not m.scrap_id
    )
    if len(moves) != 1:
        failures.append(
            f"Delivery has {len(moves)} Bench Pick Item moves, expected 1"
        )
    else:
        mv = moves[0]
        if abs((mv.quantity or 0.0) - DONE_QTY) > 1e-6:
            failures.append(
                f"Delivery Bench Pick Item Quantity (Done) is "
                f"{mv.quantity}, expected {DONE_QTY} — agent likely "
                f"forgot to edit the inline Done cell from 5 to 3"
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
            f"'{PICKING_NAME}' ({backorders.mapped('name')}) — agent "
            f"clicked 'Create Backorder' (primary default) instead of "
            f"'No Backorder' (secondary) on the validation dialog"
        )

    # ------------------------------------------------------------------
    # 3. Guard against extra outgoing pickings for this customer
    # ------------------------------------------------------------------
    all_pickings_cust = env["stock.picking"].search([
        ("partner_id", "=", customer.id),
        ("picking_type_id.code", "=", "outgoing"),
    ])
    non_cancel = all_pickings_cust.filtered(lambda p: p.state != "cancel")
    if len(non_cancel) > 1:
        failures.append(
            f"Found {len(non_cancel)} non-cancelled outgoing pickings "
            f"for '{CUSTOMER_NAME}', expected exactly 1: "
            f"{non_cancel.mapped('name')}"
        )

    # ------------------------------------------------------------------
    # 4. Stock on-hand at WH/Stock should have decreased by 3 (5 -> 2)
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
                f"expected {EXPECTED_ON_HAND} (seed=5, shipped 3, so "
                f"remaining should be 2)"
            )

    return failures
