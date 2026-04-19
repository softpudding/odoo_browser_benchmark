"""Postcondition checks for mrp.unreserve_raw_material_on_mo.

Validates that the agent clicked the statusbar **Unreserve** button on
the confirmed MO, releasing the raw-material reservation. Success means:
  * MO 'MO-BENCH-UNRES' still exists with state='confirmed' (NOT done,
    NOT cancelled, NOT renamed).
  * MO.reservation_state == 'confirmed' (was 'assigned' pre-task).
  * The single raw stock.move (for Bench Unres Mat) has state='confirmed'
    (released) — not 'assigned' (still reserved).
  * stock.quant.reserved_quantity at WH/Stock for Bench Unres Mat == 0.0.
  * stock.quant.quantity (on-hand) at WH/Stock for Bench Unres Mat ==
    10.0 (unchanged — unreserve does NOT deduct on-hand).
  * No stray MO was created or deleted.
"""

MO_NAME = "MO-BENCH-UNRES"
FINISHED = "Bench Unres Product"
COMPONENT = "Bench Unres Mat"
EXPECTED_ON_HAND = 10.0


def check(env):
    failures = []

    mo = env["mrp.production"].search([("name", "=", MO_NAME)], limit=1)
    if not mo:
        return [
            f"Manufacturing order {MO_NAME!r} not found — it must NOT be "
            f"cancelled, unlinked, or renamed. Expected state='confirmed' "
            f"with reservation_state='confirmed' after clicking Unreserve."
        ]

    # --- MO state must stay 'confirmed' (NOT cancel, NOT done) ---
    if mo.state == "cancel":
        failures.append(
            f"MO {MO_NAME!r} is cancelled — the task requires releasing "
            f"the reservation, not cancelling the MO."
        )
    elif mo.state == "done":
        failures.append(
            f"MO {MO_NAME!r} is done — the task must NOT produce / mark "
            f"done; it must only click Unreserve."
        )
    elif mo.state != "confirmed":
        failures.append(
            f"MO {MO_NAME!r} state is {mo.state!r}, expected 'confirmed'"
        )

    # --- reservation_state must be 'confirmed' (was 'assigned' pre-task) ---
    if mo.reservation_state != "confirmed":
        failures.append(
            f"MO {MO_NAME!r} reservation_state is "
            f"{mo.reservation_state!r}, expected 'confirmed' after "
            f"clicking the header Unreserve button. 'assigned' means the "
            f"Unreserve button was never clicked (or Check availability "
            f"was clicked afterwards, re-reserving)."
        )

    # --- The single raw move must be state='confirmed' (released) ---
    if len(mo.move_raw_ids) != 1:
        failures.append(
            f"Expected exactly 1 raw move on MO {MO_NAME!r}, found "
            f"{len(mo.move_raw_ids)}"
        )
    else:
        raw_move = mo.move_raw_ids
        if raw_move.product_id.name != COMPONENT:
            failures.append(
                f"Raw move product is {raw_move.product_id.name!r}, "
                f"expected {COMPONENT!r}"
            )
        if raw_move.state == "assigned":
            failures.append(
                f"Raw move state is still 'assigned' — the reservation "
                f"was NOT released. Click the statusbar Unreserve button "
                f"on MO {MO_NAME!r}."
            )
        elif raw_move.state != "confirmed":
            failures.append(
                f"Raw move state is {raw_move.state!r}, expected "
                f"'confirmed' (reservation released)"
            )
        if abs(raw_move.product_uom_qty - 5.0) > 1e-6:
            failures.append(
                f"Raw move product_uom_qty is {raw_move.product_uom_qty}, "
                f"expected 5.0 (demand must not change on unreserve)"
            )

    # --- Quant reserved_quantity and on-hand checks ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    mat = env["product.product"].search([
        ("name", "=", COMPONENT),
    ], limit=1)
    if not mat:
        failures.append(
            f"Product {COMPONENT!r} not found in DB — seed corruption?"
        )
    else:
        quants = env["stock.quant"].search([
            ("product_id", "=", mat.id),
            ("location_id", "=", stock_loc.id),
        ])
        total_reserved = sum(quants.mapped("reserved_quantity"))
        if abs(total_reserved) > 1e-6:
            failures.append(
                f"stock.quant.reserved_quantity at WH/Stock for "
                f"{COMPONENT!r} is {total_reserved}, expected 0.0 "
                f"(Unreserve should have released the 5 reserved units)"
            )
        total_on_hand = sum(quants.mapped("quantity"))
        if abs(total_on_hand - EXPECTED_ON_HAND) > 1e-6:
            failures.append(
                f"stock.quant.quantity (on-hand) at WH/Stock for "
                f"{COMPONENT!r} is {total_on_hand}, expected "
                f"{EXPECTED_ON_HAND} (on-hand must not change on unreserve)"
            )

    # --- No stray MOs for the finished product ---
    finished = env["product.product"].search([
        ("name", "=", FINISHED),
    ], limit=1)
    if finished:
        all_mos = env["mrp.production"].search([
            ("product_id", "=", finished.id),
        ])
        extra = all_mos.filtered(lambda m: m.id != mo.id)
        if extra:
            failures.append(
                f"Unexpected extra MOs for {FINISHED!r}: "
                f"{extra.mapped('name')}"
            )

    return failures
