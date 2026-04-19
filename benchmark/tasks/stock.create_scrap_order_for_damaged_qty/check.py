"""Postcondition checks for stock.create_scrap_order_for_damaged_qty.

Validates:
  1. Exactly one stock.scrap record for Bench Scrap Item with
     scrap_qty == 3.0 and state == 'done'.
  2. A stock.move with scrap_id set to that scrap, product = Bench
     Scrap Item, product_uom_qty == 3.0, state == 'done', source =
     WH/Stock, destination = a scrap (inventory-usage) location.
  3. On-hand at WH/Stock dropped from 10 to 7 (10 - 3).
"""

PRODUCT_NAME = "Bench Scrap Item"
SCRAP_QTY = 3.0


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    wh = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    stock_location = wh.lot_stock_id

    # ------------------------------------------------------------------
    # 1. Scrap record
    # ------------------------------------------------------------------
    scraps = env["stock.scrap"].with_context(active_test=False).search([
        ("product_id", "=", product.id),
    ])
    if len(scraps) == 0:
        return failures + [
            f"No stock.scrap found for '{PRODUCT_NAME}' — agent never "
            f"created the scrap order"
        ]
    if len(scraps) > 1:
        failures.append(
            f"Expected exactly 1 stock.scrap for '{PRODUCT_NAME}', found "
            f"{len(scraps)}: {scraps.mapped('name')}"
        )
    scrap = scraps[:1]

    if scrap.state != "done":
        failures.append(
            f"stock.scrap.state is '{scrap.state}', expected 'done' — "
            f"agent likely saved the draft but forgot to click Validate"
        )
    if abs((scrap.scrap_qty or 0.0) - SCRAP_QTY) > 1e-6:
        failures.append(
            f"stock.scrap.scrap_qty is {scrap.scrap_qty}, expected "
            f"{SCRAP_QTY} — agent likely left the default 1.00 instead "
            f"of typing 3"
        )
    if scrap.product_id.id != product.id:
        failures.append(
            f"stock.scrap.product_id is '{scrap.product_id.display_name}', "
            f"expected '{PRODUCT_NAME}'"
        )
    if scrap.location_id.id != stock_location.id:
        failures.append(
            f"stock.scrap.location_id is "
            f"'{scrap.location_id.complete_name}', expected "
            f"'{stock_location.complete_name}' (WH/Stock)"
        )
    # Scrap destination must be an inventory-usage location (the
    # virtual Scrap location). Odoo defaults this to the per-company
    # 'Virtual Locations/Scrap' — accept any usage='inventory' dest.
    if scrap.scrap_location_id.usage != "inventory":
        failures.append(
            f"stock.scrap.scrap_location_id is "
            f"'{scrap.scrap_location_id.complete_name}' (usage="
            f"'{scrap.scrap_location_id.usage}'), expected an inventory-"
            f"usage scrap location"
        )

    # ------------------------------------------------------------------
    # 2. Linked stock.move
    # ------------------------------------------------------------------
    moves = env["stock.move"].search([
        ("scrap_id", "=", scrap.id),
        ("product_id", "=", product.id),
    ])
    if not moves:
        # Fall back to move_ids relation on the scrap (Odoo 19 uses both).
        moves = scrap.move_ids
    if not moves:
        failures.append(
            "No stock.move linked to the scrap (scrap_id set OR "
            "scrap.move_ids). Scrap may have been validated without a "
            "move being created — unusual; check scrap.state."
        )
    else:
        scrap_moves = moves.filtered(lambda m: m.product_id.id == product.id)
        if len(scrap_moves) != 1:
            failures.append(
                f"Expected exactly 1 stock.move for the scrap, found "
                f"{len(scrap_moves)}"
            )
        else:
            mv = scrap_moves[0]
            if mv.state != "done":
                failures.append(
                    f"Scrap stock.move.state is '{mv.state}', expected "
                    f"'done' (validated scrap)"
                )
            if abs((mv.product_uom_qty or 0.0) - SCRAP_QTY) > 1e-6:
                failures.append(
                    f"Scrap stock.move.product_uom_qty is "
                    f"{mv.product_uom_qty}, expected {SCRAP_QTY}"
                )
            if mv.location_id.id != stock_location.id:
                failures.append(
                    f"Scrap stock.move.location_id is "
                    f"'{mv.location_id.complete_name}', expected "
                    f"'{stock_location.complete_name}' (WH/Stock)"
                )
            if mv.location_dest_id.usage != "inventory":
                failures.append(
                    f"Scrap stock.move.location_dest_id is "
                    f"'{mv.location_dest_id.complete_name}' (usage="
                    f"'{mv.location_dest_id.usage}'), expected inventory-"
                    f"usage scrap location"
                )

    # ------------------------------------------------------------------
    # 3. On-hand at WH/Stock dropped by 3 (10 -> 7)
    # ------------------------------------------------------------------
    on_hand = env["stock.quant"]._get_available_quantity(
        product, stock_location
    )
    if abs(on_hand - 7.0) > 1e-6:
        failures.append(
            f"WH/Stock on-hand for '{PRODUCT_NAME}' is {on_hand}, "
            f"expected 7.0 (10 seeded - 3 scrapped)"
        )

    return failures
