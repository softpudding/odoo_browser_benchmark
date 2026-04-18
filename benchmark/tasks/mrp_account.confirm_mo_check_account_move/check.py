"""Postcondition checks for mrp_account.confirm_mo_check_account_move.

Validates:
1. The MO M-BENCH-ACC-001 exists and is in 'done' state.
2. qty_produced == product_qty == 5.0 (no backorder was created).
3. At least one auto-generated account.move is linked to the MO's
   finished stock move via `stock.move.account_move_ids`.
4. Every such account.move is in the 'posted' state.
"""


MO_NAME = "M-BENCH-ACC-001"
FINISHED_NAME = "Bench Manuf Item"


def check(env):
    failures = []

    mos = env["mrp.production"].search([("name", "=", MO_NAME)])
    if not mos:
        return [f"Manufacturing order {MO_NAME!r} not found"]
    if len(mos) > 1:
        failures.append(
            f"Expected exactly 1 MO named {MO_NAME!r}, found {len(mos)}"
        )
    mo = mos[0]

    # MO state.
    if mo.state != "done":
        failures.append(f"MO state is {mo.state!r}, expected 'done'")

    # Quantities.
    if abs(mo.product_qty - 5.0) > 1e-6:
        failures.append(
            f"MO product_qty is {mo.product_qty}, expected 5.0 (do not reduce)"
        )
    if abs(mo.qty_produced - 5.0) > 1e-6:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 5.0"
        )

    # No backorder MO should exist.
    backorders = env["mrp.production"].search([
        ("name", "=like", MO_NAME + "-%"),
    ])
    if backorders:
        failures.append(
            f"Unexpected backorder MO(s) created: {backorders.mapped('name')}"
        )

    # Find the auto-generated account.move(s) linked to the MO's stock moves.
    moves = (mo.move_raw_ids | mo.move_finished_ids)
    all_amoves = env["account.move"]
    for sm in moves:
        if sm.account_move_id:
            all_amoves |= sm.account_move_id

    if not all_amoves:
        failures.append(
            "No account.move was auto-generated for the MO's stock moves. "
            "Check that the finished product uses automated (real_time) "
            "valuation and that the MO is closed."
        )
    else:
        # Every linked account move must be posted.
        not_posted = all_amoves.filtered(lambda m: m.state != "posted")
        if not_posted:
            failures.append(
                "Expected every auto-generated account.move to be 'posted'; "
                f"found non-posted: "
                f"{[(m.name or m.id, m.state) for m in not_posted]}"
            )

    # Sanity check: the MO's finished product is the expected one.
    if mo.product_id.name != FINISHED_NAME:
        failures.append(
            f"MO product is {mo.product_id.name!r}, expected {FINISHED_NAME!r}"
        )

    return failures
