"""Postcondition checks for stock.cancel_picking_create_replacement_with_serial.

Validates:
1. The original receipt R-BENCH-CANCEL-001 is in state 'cancel'.
2. The original receipt still exists (not unlinked).
3. A NEW receipt (incoming, not the original) exists for vendor Bench
   Supplier Inc, in state 'done', with a single line for Bench Serial
   Widget and demand=2.
4. That new receipt has exactly 2 stock.move.line rows for Bench Serial
   Widget, each with quantity==1 and a distinct lot_id of type
   stock.lot named BS-001 and BS-002 respectively.
5. Two stock.lot records BS-001 and BS-002 exist for Bench Serial Widget.
"""

ORIGINAL_ORIGIN = "R-BENCH-CANCEL-001"
VENDOR_NAME = "Bench Supplier Inc"
SERIAL_PRODUCT_NAME = "Bench Serial Widget"
EXPECTED_SERIALS = {"BS-001", "BS-002"}


def check(env):
    failures = []

    # ------------------------------------------------------------------
    # 1 & 2: Original picking
    # ------------------------------------------------------------------
    original = env["stock.picking"].search(
        [("origin", "=", ORIGINAL_ORIGIN)], limit=1
    )
    if not original:
        return [f"Original receipt '{ORIGINAL_ORIGIN}' not found (should be cancelled, not deleted)"]
    if original.state != "cancel":
        failures.append(
            f"Original receipt state is '{original.state}', expected 'cancel'"
        )

    # ------------------------------------------------------------------
    # 3: Replacement picking — any incoming picking for our vendor other
    #    than the original, in 'done'.
    # ------------------------------------------------------------------
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' missing"]

    serial_product = env["product.product"].search(
        [("name", "=", SERIAL_PRODUCT_NAME)], limit=1
    )
    if not serial_product:
        return [f"Product '{SERIAL_PRODUCT_NAME}' missing"]

    candidates = env["stock.picking"].search([
        ("partner_id", "=", vendor.id),
        ("picking_type_id.code", "=", "incoming"),
        ("id", "!=", original.id),
    ])
    replacement = candidates.filtered(
        lambda p: any(
            m.product_id.id == serial_product.id for m in p.move_ids
        )
    )[:1]

    if not replacement:
        failures.append(
            "No replacement receipt found for vendor 'Bench Supplier Inc' "
            "containing the 'Bench Serial Widget' product"
        )
        return failures

    if replacement.state != "done":
        failures.append(
            f"Replacement receipt state is '{replacement.state}', expected 'done'"
        )

    # Exactly one move for the serial product, demand==2.
    widget_moves = replacement.move_ids.filtered(
        lambda m: m.product_id.id == serial_product.id
    )
    if len(widget_moves) != 1:
        failures.append(
            f"Replacement receipt has {len(widget_moves)} Bench Serial Widget "
            f"moves, expected 1"
        )
    else:
        demand = widget_moves[0].product_uom_qty
        if abs(demand - 2.0) > 0.001:
            failures.append(
                f"Replacement demand for Bench Serial Widget is {demand}, expected 2.0"
            )

    # No other products on replacement.
    extra = replacement.move_ids.filtered(
        lambda m: m.product_id.id != serial_product.id
    )
    if extra:
        names = ", ".join(sorted(set(extra.mapped("product_id.name"))))
        failures.append(
            f"Replacement receipt has extra product moves: {names}"
        )

    # ------------------------------------------------------------------
    # 4: Move lines — two rows, each qty 1, distinct lots.
    # ------------------------------------------------------------------
    if widget_moves:
        mls = widget_moves.mapped("move_line_ids")
        # Only consider done move lines with positive quantity.
        real_mls = mls.filtered(lambda ml: ml.quantity > 0)
        if len(real_mls) != 2:
            failures.append(
                f"Expected 2 move_lines (qty>0) for Bench Serial Widget, found {len(real_mls)} "
                f"— agent likely merged both serials into a single move_line"
            )
        else:
            qtys = sorted(ml.quantity for ml in real_mls)
            if not all(abs(q - 1.0) < 0.001 for q in qtys):
                failures.append(
                    f"Move line quantities are {qtys}, expected [1.0, 1.0]"
                )

        lot_names = set()
        for ml in real_mls:
            if ml.lot_id:
                lot_names.add(ml.lot_id.name)
        missing = EXPECTED_SERIALS - lot_names
        extra_lots = lot_names - EXPECTED_SERIALS
        if missing:
            failures.append(
                f"Missing serials on move_lines: {sorted(missing)} "
                f"(found {sorted(lot_names)})"
            )
        if extra_lots:
            failures.append(
                f"Unexpected serials on move_lines: {sorted(extra_lots)}"
            )

    # ------------------------------------------------------------------
    # 5: stock.lot records
    # ------------------------------------------------------------------
    for sn in EXPECTED_SERIALS:
        lot = env["stock.lot"].search([
            ("name", "=", sn),
            ("product_id", "=", serial_product.id),
        ], limit=1)
        if not lot:
            failures.append(
                f"stock.lot record '{sn}' for Bench Serial Widget was not created"
            )

    return failures
