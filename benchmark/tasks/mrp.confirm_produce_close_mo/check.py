"""Postcondition checks for mrp.confirm_produce_close_mo.

Validates:
1. MO WH/MO/BENCH-DESK-001 exists and is in 'done' state.
2. qty_produced == product_qty == 10.0 (no backorder was created).
3. The MO is locked (Odoo sets is_locked=True after button_mark_done).
4. The three component raw moves (Desk Top, Desk Leg, Cable Tray) are
   all 'done' with the expected BoM-scaled quantities.
5. No backorder MO was created.
"""


MO_NAME = "WH/MO/BENCH-DESK-001"
EXPECTED_RAW = {
    "Desk Top": 10.0,
    "Desk Leg": 40.0,
    "Cable Tray": 10.0,
}


def check(env):
    failures = []

    mos = env["mrp.production"].search([("name", "=", MO_NAME)])
    if not mos:
        return [f"Manufacturing order {MO_NAME!r} not found"]
    if len(mos) > 1:
        failures.append(f"Expected exactly 1 MO named {MO_NAME!r}, found {len(mos)}")
    mo = mos[0]

    if mo.state != "done":
        failures.append(f"MO state is {mo.state!r}, expected 'done'")

    if mo.product_qty != 10.0:
        failures.append(
            f"MO product_qty is {mo.product_qty}, expected 10.0 (do not reduce)"
        )

    if mo.qty_produced != 10.0:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 10.0"
        )

    if not mo.is_locked:
        failures.append("MO is not locked (should be locked after done)")

    # No backorder MO should have been created.
    backorders = env["mrp.production"].search([
        ("name", "=like", MO_NAME + "-%"),
    ])
    if backorders:
        failures.append(
            f"Unexpected backorder MO(s) created: {backorders.mapped('name')}"
        )

    # Raw moves should all be 'done' with expected consumed quantities.
    raw_by_name = {}
    for move in mo.move_raw_ids:
        raw_by_name[move.product_id.display_name] = move

    for comp_name, expected_qty in EXPECTED_RAW.items():
        move = raw_by_name.get(comp_name)
        if not move:
            failures.append(f"Raw move for component {comp_name!r} missing")
            continue
        if move.state != "done":
            failures.append(
                f"Raw move for {comp_name!r} is in state {move.state!r}, expected 'done'"
            )
        # After button_mark_done, product_uom_qty may be re-written; use
        # quantity (the actual done quantity) instead.
        if abs(move.quantity - expected_qty) > 1e-6:
            failures.append(
                f"Raw move for {comp_name!r} consumed {move.quantity}, "
                f"expected {expected_qty}"
            )

    # The finished-goods move should be done for 10 units.
    finished_moves = mo.move_finished_ids.filtered(
        lambda m: m.product_id == mo.product_id
    )
    if not finished_moves:
        failures.append("No finished-goods stock move found for the MO")
    else:
        fm = finished_moves[0]
        if fm.state != "done":
            failures.append(
                f"Finished move state is {fm.state!r}, expected 'done'"
            )
        if abs(fm.quantity - 10.0) > 1e-6:
            failures.append(
                f"Finished move quantity is {fm.quantity}, expected 10.0"
            )

    return failures
