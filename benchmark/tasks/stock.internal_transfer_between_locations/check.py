"""Postcondition checks for stock.internal_transfer_between_locations."""


PRODUCT_NAME = "Benchmark Shelf Widget"
ORIGIN = "BENCH-INT-SHELF-A1"


def check(env):
    failures = []

    pickings = env["stock.picking"].search([("origin", "=", ORIGIN)])
    if not pickings:
        return [f"No internal transfer with origin '{ORIGIN}' found"]
    if len(pickings) > 1:
        failures.append(f"Found {len(pickings)} transfers, expected 1")
    pick = pickings[0]

    if pick.state != "done":
        failures.append(
            f"Transfer state is '{pick.state}', expected 'done' (validated)"
        )

    # Source and destination location checks.
    src_name = pick.location_id.complete_name or pick.location_id.name or ""
    dest_name = (
        pick.location_dest_id.complete_name
        or pick.location_dest_id.name
        or ""
    )
    if src_name != "WH/Stock":
        failures.append(
            f"Source location is '{src_name}', expected 'WH/Stock'"
        )
    if dest_name != "WH/Stock/Shelf A1":
        failures.append(
            f"Destination location is '{dest_name}', expected "
            f"'WH/Stock/Shelf A1'"
        )

    # Picking type must be internal.
    if pick.picking_type_id.code != "internal":
        failures.append(
            f"Picking type is '{pick.picking_type_id.code}', expected 'internal'"
        )

    # Moves: exactly one line for the target product, qty 5.
    moves = pick.move_ids
    if len(moves) != 1:
        failures.append(f"Expected 1 move line, found {len(moves)}")
    for m in moves:
        if m.product_id.name != PRODUCT_NAME:
            failures.append(
                f"Move product is '{m.product_id.name}', expected "
                f"'{PRODUCT_NAME}'"
            )
        if abs((m.quantity or 0.0) - 5.0) > 1e-6:
            failures.append(
                f"Move done quantity is {m.quantity}, expected 5"
            )

    return failures
