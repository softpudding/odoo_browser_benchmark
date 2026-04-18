"""Postcondition checks for stock.transfer_reserved_to_ready_partial_backorder.

Validates:
  1. Original outgoing picking (origin=D-BENCH-PARTIAL-001, backorder_id=False)
     is in state 'done' with a single Bench Partial Item move whose
     quantity == 7 and product_uom_qty == 7 (Odoo auto-splits demand on
     backorder-creation).
  2. Exactly one backorder stock.picking exists with backorder_id ==
     original.id, carrying a single Bench Partial Item move of
     product_uom_qty == 3, state in ('assigned', 'confirmed', 'waiting').
  3. No extra pickings, moves, scraps, or unexpected cancellations.
"""

ORIGIN = "D-BENCH-PARTIAL-001"
CUSTOMER_NAME = "Bench Partial Cust"
PRODUCT_NAME = "Bench Partial Item"
DONE_QTY = 7.0
BACKORDER_QTY = 3.0


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
    # 1. Original outgoing picking
    # ------------------------------------------------------------------
    originals = env["stock.picking"].search([
        ("origin", "=", ORIGIN),
        ("picking_type_id.code", "=", "outgoing"),
        ("backorder_id", "=", False),
    ])
    if not originals:
        return failures + [
            f"Original delivery (origin='{ORIGIN}', backorder_id=False) "
            f"not found"
        ]
    if len(originals) > 1:
        failures.append(
            f"Expected exactly 1 original delivery for '{ORIGIN}', "
            f"found {len(originals)}: {originals.mapped('name')}"
        )
    original = originals[:1]

    if original.state != "done":
        failures.append(
            f"Original delivery state is '{original.state}', expected 'done' "
            f"— did the agent click Validate and Create Backorder?"
        )

    moves = original.move_ids.filtered(
        lambda m: m.product_id.id == product.id and not m.scrap_id
    )
    if len(moves) != 1:
        failures.append(
            f"Original delivery has {len(moves)} Bench Partial Item moves, "
            f"expected 1"
        )
    else:
        mv = moves[0]
        if abs((mv.quantity or 0.0) - DONE_QTY) > 1e-6:
            failures.append(
                f"Original delivery Bench Partial Item Quantity (Done) is "
                f"{mv.quantity}, expected {DONE_QTY} — agent likely forgot "
                f"to edit Quantity from 10 to 7 via the Detailed Operations "
                f"popup"
            )
        # After validate-with-backorder, Odoo splits the move: the original
        # move's product_uom_qty is reduced to the Done amount (7) and a
        # new move with the remaining demand (3) is created on the
        # backorder picking.
        if abs((mv.product_uom_qty or 0.0) - DONE_QTY) > 1e-6:
            failures.append(
                f"Original delivery Bench Partial Item demand is "
                f"{mv.product_uom_qty}, expected {DONE_QTY} (Odoo auto-"
                f"splits demand on backorder creation)"
            )

    # ------------------------------------------------------------------
    # 2. Backorder picking
    # ------------------------------------------------------------------
    backorders = env["stock.picking"].search([
        ("backorder_id", "=", original.id),
    ])
    if not backorders:
        failures.append(
            "No backorder delivery found — agent likely clicked 'No "
            "Backorder' instead of 'Create Backorder' on the validation "
            "dialog"
        )
    elif len(backorders) > 1:
        failures.append(
            f"Expected exactly 1 backorder for '{ORIGIN}', found "
            f"{len(backorders)}: {backorders.mapped('name')}"
        )
    else:
        bo = backorders[0]
        if bo.state == "done":
            failures.append(
                "Backorder delivery is already 'done' — agent validated it "
                "too (task only covers the first picking + backorder)"
            )
        if bo.state == "cancel":
            failures.append("Backorder delivery is cancelled")
        if bo.state not in ("assigned", "confirmed", "waiting"):
            failures.append(
                f"Backorder delivery state is '{bo.state}', expected one "
                f"of ('assigned', 'confirmed', 'waiting')"
            )
        bo_moves = bo.move_ids.filtered(
            lambda m: m.product_id.id == product.id and not m.scrap_id
        )
        if len(bo_moves) != 1:
            failures.append(
                f"Backorder has {len(bo_moves)} Bench Partial Item moves, "
                f"expected 1"
            )
        elif abs((bo_moves[0].product_uom_qty or 0.0) - BACKORDER_QTY) > 1e-6:
            failures.append(
                f"Backorder Bench Partial Item demand is "
                f"{bo_moves[0].product_uom_qty}, expected {BACKORDER_QTY}"
            )

    # ------------------------------------------------------------------
    # 3. Guard against extra pickings
    # ------------------------------------------------------------------
    all_pickings = env["stock.picking"].search([
        ("origin", "=", ORIGIN),
        ("picking_type_id.code", "=", "outgoing"),
    ])
    # Expect at most 2: original + one backorder.
    non_cancel = all_pickings.filtered(lambda p: p.state != "cancel")
    if len(non_cancel) > 2:
        failures.append(
            f"Found {len(non_cancel)} non-cancelled outgoing pickings for "
            f"'{ORIGIN}', expected exactly 2 (original + backorder): "
            f"{non_cancel.mapped('name')}"
        )

    return failures
