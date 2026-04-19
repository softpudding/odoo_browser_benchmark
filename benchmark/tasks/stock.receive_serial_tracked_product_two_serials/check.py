"""Postcondition checks for stock.receive_serial_tracked_product_two_serials.

Validates:
  1. The picking WH/IN/BENCH-SERIAL is in state 'done'.
  2. It has exactly one Bench Serial Item move with demand == 2.
  3. That move has exactly 2 stock.move.line rows (qty > 0), each with
     quantity == 1 and a distinct lot_id bearing one of the expected
     serial names.
  4. Exactly 2 stock.lot records for Bench Serial Item exist with names
     SN-BENCH-A001 and SN-BENCH-A002.
  5. No backorder picking was created.
  6. No extra incoming pickings for the vendor beyond the one expected.
"""

PICKING_NAME = "WH/IN/BENCH-SERIAL"
VENDOR_NAME = "Bench Serial Vendor"
PRODUCT_NAME = "Bench Serial Item"
EXPECTED_DEMAND = 2.0
EXPECTED_SERIALS = {"SN-BENCH-A001", "SN-BENCH-A002"}


def check(env):
    failures = []

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    # ------------------------------------------------------------------
    # 1. Original picking by pinned name
    # ------------------------------------------------------------------
    pickings = env["stock.picking"].search([
        ("name", "=", PICKING_NAME),
        ("picking_type_id.code", "=", "incoming"),
    ])
    if not pickings:
        return failures + [
            f"Incoming receipt '{PICKING_NAME}' not found — did the "
            f"agent cancel or unlink it?"
        ]
    if len(pickings) > 1:
        failures.append(
            f"Expected exactly 1 receipt named '{PICKING_NAME}', "
            f"found {len(pickings)}"
        )
    picking = pickings[:1]

    if picking.state != "done":
        failures.append(
            f"Receipt '{PICKING_NAME}' state is '{picking.state}', "
            f"expected 'done' — did the agent click Validate after "
            f"entering both serials?"
        )

    # ------------------------------------------------------------------
    # 2. Single Bench Serial Item move, demand unchanged
    # ------------------------------------------------------------------
    moves = picking.move_ids.filtered(
        lambda m: m.product_id.id == product.id and not m.scrap_id
    )
    if len(moves) != 1:
        failures.append(
            f"Receipt has {len(moves)} Bench Serial Item moves, "
            f"expected 1"
        )
    else:
        move = moves[0]
        if abs(move.product_uom_qty - EXPECTED_DEMAND) > 1e-6:
            failures.append(
                f"Bench Serial Item demand is {move.product_uom_qty}, "
                f"expected {EXPECTED_DEMAND} — agent must not change "
                f"Demand"
            )

    # Guard against extra products on the picking.
    extra = picking.move_ids.filtered(
        lambda m: m.product_id.id != product.id and not m.scrap_id
    )
    if extra:
        names = ", ".join(sorted(set(extra.mapped("product_id.name"))))
        failures.append(
            f"Receipt has extra product moves (should only have Bench "
            f"Serial Item): {names}"
        )

    # ------------------------------------------------------------------
    # 3. Move lines — exactly 2, qty=1 each, distinct serial lots
    # ------------------------------------------------------------------
    if moves:
        mls = moves.mapped("move_line_ids")
        real_mls = mls.filtered(lambda ml: (ml.quantity or 0.0) > 0)
        if len(real_mls) != 2:
            failures.append(
                f"Expected 2 move_lines (qty>0) for Bench Serial Item, "
                f"found {len(real_mls)} — agent likely merged both "
                f"serials into a single move_line (qty=2) instead of "
                f"adding a second row in the Detailed Operations popup"
            )
        else:
            qtys = sorted(ml.quantity for ml in real_mls)
            if not all(abs(q - 1.0) < 1e-6 for q in qtys):
                failures.append(
                    f"Move line quantities are {qtys}, expected "
                    f"[1.0, 1.0]"
                )

        lot_names = set()
        for ml in real_mls:
            if ml.lot_id:
                lot_names.add(ml.lot_id.name)
            elif ml.lot_name:
                # Defensive — some flows persist lot_name instead of
                # lot_id on a pristine move line. Treat this as a failure
                # because we require the stock.lot rows to exist.
                pass
        missing = EXPECTED_SERIALS - lot_names
        extra_lots = lot_names - EXPECTED_SERIALS
        if missing:
            failures.append(
                f"Missing serials on move_lines: {sorted(missing)} "
                f"(found {sorted(lot_names)})"
            )
        if extra_lots:
            failures.append(
                f"Unexpected serials on move_lines: "
                f"{sorted(extra_lots)}"
            )

    # ------------------------------------------------------------------
    # 4. stock.lot records
    # ------------------------------------------------------------------
    for sn in EXPECTED_SERIALS:
        lot = env["stock.lot"].search([
            ("name", "=", sn),
            ("product_id", "=", product.id),
        ], limit=1)
        if not lot:
            failures.append(
                f"stock.lot record '{sn}' for Bench Serial Item was "
                f"not created"
            )

    # ------------------------------------------------------------------
    # 5. No backorder pickings for the original
    # ------------------------------------------------------------------
    backorders = env["stock.picking"].search([
        ("backorder_id", "=", picking.id),
    ])
    if backorders:
        failures.append(
            f"Found {len(backorders)} backorder picking(s) for "
            f"'{PICKING_NAME}' ({backorders.mapped('name')}) — since "
            f"both serials should be validated together, no backorder "
            f"should exist"
        )

    # ------------------------------------------------------------------
    # 6. No extra incoming pickings for the vendor
    # ------------------------------------------------------------------
    all_pickings_vnd = env["stock.picking"].search([
        ("partner_id", "=", vendor.id),
        ("picking_type_id.code", "=", "incoming"),
    ])
    non_cancel = all_pickings_vnd.filtered(lambda p: p.state != "cancel")
    if len(non_cancel) > 1:
        failures.append(
            f"Found {len(non_cancel)} non-cancelled incoming pickings "
            f"for '{VENDOR_NAME}', expected exactly 1: "
            f"{non_cancel.mapped('name')}"
        )

    return failures
