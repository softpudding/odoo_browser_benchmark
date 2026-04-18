"""Postcondition checks for sale_stock.partial_stock_warning_confirm_anyway.

Validates:
1. SO with client_order_ref 'S-BENCH-STK-001' is confirmed (state='sale').
2. Exactly two pickings exist for the SO:
   - Original: state='done', move Done quantity = 2.
   - Backorder (backorder_id = original): state != 'cancel', move demand = 8.
3. No extra stray pickings for this SO.
"""


def check(env):
    failures = []

    so = env["sale.order"].search(
        [("client_order_ref", "=", "S-BENCH-STK-001")], limit=1
    )
    if not so:
        return ["Target SO 'S-BENCH-STK-001' not found"]

    if so.state != "sale":
        failures.append(f"SO state is '{so.state}', expected 'sale'")

    pickings = so.picking_ids
    if not pickings:
        return failures + ["No delivery orders found for the SO"]

    # Expect exactly 2 pickings (original + one backorder).
    # Ignore cancelled ones from the count.
    active_pickings = pickings.filtered(lambda p: p.state != "cancel")
    if len(active_pickings) != 2:
        failures.append(
            f"Expected exactly 2 active pickings for SO, found "
            f"{len(active_pickings)} (states: "
            f"{[p.state for p in active_pickings]})"
        )

    # Original: the one without backorder_id.
    original = pickings.filtered(lambda p: not p.backorder_id)
    backorders = pickings.filtered(lambda p: p.backorder_id)

    if len(original) != 1:
        return failures + [
            f"Expected exactly 1 original (non-backorder) picking, "
            f"found {len(original)}"
        ]

    original = original[0]
    if original.state != "done":
        failures.append(
            f"Original delivery state is '{original.state}', expected 'done'"
        )

    # Check Done quantity on the original delivery = 2.
    # In Odoo 19 the Done column on stock.move is 'quantity'.
    orig_move = original.move_ids
    if len(orig_move) != 1:
        failures.append(
            f"Original delivery has {len(orig_move)} moves, expected 1"
        )
    elif "Bench Limited Widget" not in orig_move.product_id.name:
        failures.append(
            f"Original delivery move product is "
            f"'{orig_move.product_id.name}', expected 'Bench Limited Widget'"
        )
    else:
        qty = getattr(orig_move, "quantity", None)
        if qty is None:
            qty = getattr(orig_move, "quantity_done", 0.0)
        if abs(qty - 2.0) > 0.001:
            failures.append(
                f"Original delivery Done quantity is {qty}, expected 2"
            )
        # Ordered demand must still be the originally-split amount (2 on this
        # picking after backorder split). Accept either 2 (after split) or 10
        # (if no split happened).
        demand = orig_move.product_uom_qty
        if abs(demand - 2.0) > 0.001 and abs(demand - 10.0) > 0.001:
            failures.append(
                f"Original delivery move demand is {demand}, "
                f"expected 2 or 10"
            )

    # Must have exactly one backorder with the 8 remaining units.
    backorders_linked = backorders.filtered(
        lambda p: p.backorder_id.id == original.id
    )
    if len(backorders_linked) != 1:
        failures.append(
            f"Expected exactly 1 backorder linked to original, "
            f"found {len(backorders_linked)}"
        )
    else:
        bo = backorders_linked[0]
        if bo.state == "cancel":
            failures.append(
                f"Backorder state is 'cancel', expected ready/assigned/waiting"
            )
        bo_moves = bo.move_ids
        if len(bo_moves) != 1:
            failures.append(
                f"Backorder has {len(bo_moves)} moves, expected 1"
            )
        else:
            bo_move = bo_moves[0]
            if "Bench Limited Widget" not in bo_move.product_id.name:
                failures.append(
                    f"Backorder move product is "
                    f"'{bo_move.product_id.name}', "
                    f"expected 'Bench Limited Widget'"
                )
            if abs(bo_move.product_uom_qty - 8.0) > 0.001:
                failures.append(
                    f"Backorder move demand is {bo_move.product_uom_qty}, "
                    f"expected 8"
                )

    return failures
