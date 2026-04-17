"""Postcondition checks for mrp.produce_and_close_mo.

Validates:
1. MO WH/MO/BENCH-001 exists and is in 'done' state.
2. The quantity produced matches the ordered quantity (5).
3. The MO is locked.
"""


def check(env):
    failures = []

    mo = env["mrp.production"].search([
        ("name", "=", "WH/MO/BENCH-001"),
    ], limit=1)
    if not mo:
        return ["Manufacturing order 'WH/MO/BENCH-001' not found"]

    if mo.state != "done":
        failures.append(
            f"MO state is '{mo.state}', expected 'done'"
        )

    if mo.qty_produced != 5.0:
        failures.append(
            f"Qty produced is {mo.qty_produced}, expected 5.0"
        )

    if not mo.is_locked:
        failures.append("MO is not locked (should be locked after done)")

    return failures
