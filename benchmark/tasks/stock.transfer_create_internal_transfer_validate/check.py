"""Postcondition checks for stock.transfer_create_internal_transfer_validate.

Validates:
  1. Exactly one non-cancelled internal stock.picking for Bench Move Item
     exists, in state='done', with source WH/Stock and destination
     WH/Stock/Shelf C.
  2. It has exactly one Bench Move Item move with quantity==5 (Done).
  3. picking_type_id.code == 'internal'.
  4. A stock.quant at WH/Stock/Shelf C for Bench Move Item with
     quantity==5 exists.
  5. The WH/Stock quant for Bench Move Item is reduced to 5 (from 10).
  6. Product integrity: type='consu' + is_storable=True (unchanged).
"""

PRODUCT_NAME = "Bench Move Item"
LOCATION_SRC = "WH/Stock"
LOCATION_DEST = "WH/Stock/Shelf C"
EXPECTED_QTY = 5.0
EXPECTED_STOCK_QTY = 5.0


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found (seed issue)"]

    # Product integrity
    if product.type != "consu":
        failures.append(
            f"Product type is '{product.type}', expected 'consu'"
        )
    if not product.is_storable:
        failures.append(
            "Product is_storable is False, expected True"
        )

    # -----------------------------------------------------------------
    # 1. Internal pickings touching the product.
    # -----------------------------------------------------------------
    all_pickings = env["stock.picking"].search([
        ("move_ids.product_id", "=", product.id),
        ("picking_type_id.code", "=", "internal"),
    ])
    non_cancel = all_pickings.filtered(lambda p: p.state != "cancel")
    if not non_cancel:
        return failures + [
            "No internal stock.picking for Bench Move Item found — "
            "agent never created the transfer"
        ]
    if len(non_cancel) > 1:
        failures.append(
            f"Expected exactly 1 non-cancelled internal transfer for "
            f"'{PRODUCT_NAME}', found {len(non_cancel)}: "
            f"{non_cancel.mapped('name')}"
        )

    pick = non_cancel[:1]

    # 2. state must be done
    if pick.state != "done":
        failures.append(
            f"Internal transfer state is '{pick.state}', expected 'done' "
            f"— did you click Mark as Todo then Validate?"
        )

    # 3. picking type is internal (extra defense)
    if pick.picking_type_id.code != "internal":
        failures.append(
            f"picking_type_id.code is '{pick.picking_type_id.code}', "
            f"expected 'internal'"
        )

    # 4. Source + destination locations
    src_name = pick.location_id.complete_name or pick.location_id.name
    dest_name = (
        pick.location_dest_id.complete_name or pick.location_dest_id.name
    )
    if src_name != LOCATION_SRC:
        failures.append(
            f"Source location is '{src_name}', expected '{LOCATION_SRC}'"
        )
    if dest_name != LOCATION_DEST:
        failures.append(
            f"Destination location is '{dest_name}', expected "
            f"'{LOCATION_DEST}' — agent likely left the default WH/Stock"
        )

    # 5. Moves: exactly one Bench Move Item move, qty=5
    moves = pick.move_ids.filtered(
        lambda m: m.product_id.id == product.id and not m.scrap_id
    )
    if len(moves) != 1:
        failures.append(
            f"Internal transfer has {len(moves)} '{PRODUCT_NAME}' moves, "
            f"expected 1"
        )
    else:
        mv = moves[0]
        if abs((mv.quantity or 0.0) - EXPECTED_QTY) > 1e-6:
            failures.append(
                f"Move Quantity (Done) is {mv.quantity}, expected "
                f"{EXPECTED_QTY}"
            )
        if abs((mv.product_uom_qty or 0.0) - EXPECTED_QTY) > 1e-6:
            failures.append(
                f"Move Demand is {mv.product_uom_qty}, expected "
                f"{EXPECTED_QTY}"
            )

    # Guard against stray additional moves (e.g., phantom empty second
    # row) — the picking should have no moves beyond the Bench Move Item.
    other_moves = pick.move_ids.filtered(
        lambda m: m.product_id.id != product.id and not m.scrap_id
    )
    if other_moves:
        failures.append(
            f"Internal transfer has {len(other_moves)} extra moves "
            f"beyond '{PRODUCT_NAME}': "
            f"{other_moves.mapped('product_id.name')}"
        )

    # 6. Quants: WH/Stock/Shelf C has 5, WH/Stock has 5 (originally 10).
    shelf = env["stock.location"].search([
        ("complete_name", "=", LOCATION_DEST),
    ], limit=1)
    stock_loc = env["stock.location"].search([
        ("complete_name", "=", LOCATION_SRC),
        ("usage", "=", "internal"),
    ], limit=1)

    if shelf:
        shelf_quants = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", shelf.id),
        ])
        shelf_qty = sum(q.quantity for q in shelf_quants)
        if abs(shelf_qty - EXPECTED_QTY) > 1e-6:
            failures.append(
                f"Quant at '{LOCATION_DEST}' for '{PRODUCT_NAME}' is "
                f"{shelf_qty}, expected {EXPECTED_QTY} (a validated "
                f"internal transfer for 5 should create a 5-unit quant "
                f"at the destination)"
            )
    else:
        failures.append(
            f"Destination sub-location '{LOCATION_DEST}' not found"
        )

    if stock_loc:
        stock_quants = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", stock_loc.id),
        ])
        stock_qty = sum(q.quantity for q in stock_quants)
        if abs(stock_qty - EXPECTED_STOCK_QTY) > 1e-6:
            failures.append(
                f"Quant at '{LOCATION_SRC}' for '{PRODUCT_NAME}' is "
                f"{stock_qty}, expected {EXPECTED_STOCK_QTY} (seeded 10, "
                f"moved 5 to Shelf C, so remainder should be 5)"
            )

    return failures
