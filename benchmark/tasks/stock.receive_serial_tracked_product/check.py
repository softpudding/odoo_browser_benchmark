"""Postcondition checks for stock.receive_serial_tracked_product.

Verifies:
1. The seeded receipt (origin BENCH-SN-RCV-01) reached state='done'.
2. Exactly three stock.lot records named SN-BENCH-001/002/003 exist
   for the Bench Serial Gadget product.
3. The receipt has exactly three move.lines for the product, each
   with quantity 1 and a distinct lot_id matching the expected set.
4. Three stock.quant records (qty 1 each) sit at WH/Stock for the
   three serials after validation.
"""

PRODUCT_NAME = "Bench Serial Gadget"
RECEIPT_ORIGIN = "BENCH-SN-RCV-01"
EXPECTED_SERIALS = {"SN-BENCH-001", "SN-BENCH-002", "SN-BENCH-003"}


def check(env):
    failures = []

    picking = env["stock.picking"].search(
        [("origin", "=", RECEIPT_ORIGIN)], limit=1
    )
    if not picking:
        return [f"Receipt with origin '{RECEIPT_ORIGIN}' not found"]

    if picking.state != "done":
        failures.append(
            f"Receipt state is '{picking.state}', expected 'done' — "
            f"agent likely failed to validate after assigning three serials"
        )

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    if product.tracking != "serial":
        failures.append(
            f"Product tracking is '{product.tracking}', expected 'serial'"
        )

    # Lots: exactly three with the expected names tied to this product.
    lots = env["stock.lot"].search(
        [
            ("product_id", "=", product.id),
            ("name", "in", list(EXPECTED_SERIALS)),
        ]
    )
    lot_names = set(lots.mapped("name"))
    missing = EXPECTED_SERIALS - lot_names
    if missing:
        failures.append(
            f"Missing serial lots for '{PRODUCT_NAME}': {sorted(missing)}"
        )

    all_lots = env["stock.lot"].search(
        [("product_id", "=", product.id)]
    )
    extra = set(all_lots.mapped("name")) - EXPECTED_SERIALS
    if extra:
        failures.append(
            f"Unexpected extra serial lots for '{PRODUCT_NAME}': {sorted(extra)}"
        )

    # Move lines — three with qty 1 each, distinct lots, on the receipt.
    moves = picking.move_ids.filtered(lambda m: m.product_id.id == product.id)
    if len(moves) != 1:
        failures.append(
            f"Expected exactly 1 move for {PRODUCT_NAME} on the receipt, "
            f"found {len(moves)}"
        )
    else:
        mls = moves.move_line_ids.filtered(lambda ml: ml.quantity > 0)
        if len(mls) != 3:
            failures.append(
                f"Expected exactly 3 move lines (qty>0) on the receipt for "
                f"{PRODUCT_NAME}, found {len(mls)} — agent likely merged "
                f"serials onto a single move line"
            )
        else:
            qtys = sorted(ml.quantity for ml in mls)
            if not all(abs(q - 1.0) < 0.001 for q in qtys):
                failures.append(
                    f"Move line quantities are {qtys}, expected [1.0, 1.0, 1.0]"
                )

            lot_names_on_mls = set()
            for ml in mls:
                if ml.lot_id:
                    lot_names_on_mls.add(ml.lot_id.name)
            if lot_names_on_mls != EXPECTED_SERIALS:
                failures.append(
                    f"Move line serials are {sorted(lot_names_on_mls)}, "
                    f"expected {sorted(EXPECTED_SERIALS)}"
                )

    # Quants — each serial at WH/Stock with quantity 1.
    if picking.state == "done":
        stock_loc = env["stock.location"].search(
            [("complete_name", "=", "WH/Stock")], limit=1
        )
        if stock_loc and lots:
            for lot in lots:
                quant = env["stock.quant"].search(
                    [
                        ("product_id", "=", product.id),
                        ("location_id", "=", stock_loc.id),
                        ("lot_id", "=", lot.id),
                    ],
                    limit=1,
                )
                if not quant:
                    failures.append(
                        f"No stock.quant at WH/Stock for serial '{lot.name}'"
                    )
                elif abs(quant.quantity - 1.0) > 0.001:
                    failures.append(
                        f"Quant for serial '{lot.name}' has quantity "
                        f"{quant.quantity}, expected 1.0"
                    )

    return failures
