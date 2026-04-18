"""Postcondition checks for sale_stock.deliver_partial_split_into_two_pickings.

Validates:
1. SO 'S-BENCH-SPLIT-001' is confirmed (state='sale').
2. Exactly two non-cancelled pickings exist for the SO:
   - Original (no backorder_id): state='done', Alpha Done=5, Beta Done=3.
   - Backorder (backorder_id=original.id): state in (draft, assigned,
     waiting, confirmed) — NOT done, NOT cancel — with one move for
     Halberd Beta Module of demand=5 and Done=0 (zeroed by the agent).
"""


def check(env):
    failures = []

    so = env["sale.order"].search(
        [("client_order_ref", "=", "S-BENCH-SPLIT-001")], limit=1
    )
    if not so:
        return ["Target SO 'S-BENCH-SPLIT-001' not found"]

    if so.state != "sale":
        failures.append(f"SO state is '{so.state}', expected 'sale'")

    pickings = so.picking_ids
    if not pickings:
        return failures + ["No delivery orders found for the SO"]

    active = pickings.filtered(lambda p: p.state != "cancel")
    if len(active) != 2:
        failures.append(
            f"Expected exactly 2 active pickings (original + backorder), "
            f"found {len(active)} (states: {[p.state for p in active]})"
        )

    originals = pickings.filtered(lambda p: not p.backorder_id)
    backorders = pickings.filtered(lambda p: p.backorder_id)

    if len(originals) != 1:
        return failures + [
            f"Expected exactly 1 original (non-backorder) picking, "
            f"found {len(originals)}"
        ]
    original = originals[0]

    # --- Original picking: must be done, Alpha=5, Beta=3 ---
    if original.state != "done":
        failures.append(
            f"Original delivery state is '{original.state}', expected 'done'"
        )

    moves = original.move_ids
    alpha_move = moves.filtered(lambda m: "Alpha" in m.product_id.name)
    beta_move = moves.filtered(lambda m: "Beta" in m.product_id.name)

    if not alpha_move:
        failures.append("Halberd Alpha Module move missing on original picking")
    else:
        amove = alpha_move[0]
        qty = getattr(amove, "quantity", None)
        if qty is None:
            qty = getattr(amove, "quantity_done", 0.0)
        if abs(qty - 5.0) > 0.001:
            failures.append(
                f"Original picking Alpha Done qty is {qty}, expected 5"
            )

    if not beta_move:
        failures.append("Halberd Beta Module move missing on original picking")
    else:
        bmove = beta_move[0]
        qty = getattr(bmove, "quantity", None)
        if qty is None:
            qty = getattr(bmove, "quantity_done", 0.0)
        if abs(qty - 3.0) > 0.001:
            failures.append(
                f"Original picking Beta Done qty is {qty}, expected 3"
            )

    # --- Backorder picking: not done, not cancel, Beta only, demand=5,
    #     Done = 0 (agent must have zeroed it).
    backorders_active = backorders.filtered(lambda p: p.state != "cancel")
    if len(backorders_active) != 1:
        failures.append(
            f"Expected exactly 1 active backorder linked to original, "
            f"found {len(backorders_active)}"
        )
        return failures

    bo = backorders_active[0]
    if bo.backorder_id.id != original.id:
        failures.append(
            f"Backorder picking is not linked to the original picking "
            f"(backorder_id={bo.backorder_id.id}, expected {original.id})"
        )

    if bo.state == "done":
        failures.append(
            "Backorder is in state 'done' — the agent must NOT have validated "
            "the backorder; it must remain assigned/draft with Done=0 saved"
        )

    bo_moves = bo.move_ids
    if len(bo_moves) != 1:
        failures.append(
            f"Backorder has {len(bo_moves)} moves, expected exactly 1 (Beta)"
        )
    else:
        bm = bo_moves[0]
        if "Beta" not in bm.product_id.name:
            failures.append(
                f"Backorder move product is '{bm.product_id.name}', "
                f"expected 'Halberd Beta Module'"
            )
        if abs(bm.product_uom_qty - 5.0) > 0.001:
            failures.append(
                f"Backorder move demand is {bm.product_uom_qty}, expected 5"
            )
        # The agent must have zeroed Done from the auto-reserved 5 -> 0.
        qty = getattr(bm, "quantity", None)
        if qty is None:
            qty = getattr(bm, "quantity_done", 0.0)
        if abs(qty - 0.0) > 0.001:
            failures.append(
                f"Backorder Beta Done qty is {qty}, expected 0 "
                f"(agent must have edited it from 5 down to 0)"
            )

    return failures
