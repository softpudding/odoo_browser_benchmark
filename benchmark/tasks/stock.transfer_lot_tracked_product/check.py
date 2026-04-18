"""Postconditions for stock.transfer_lot_tracked_product."""

PRODUCT_NAME = "Lot Product A"
RECEIPT_ORIGIN = "BENCH-TRANSFER-LOT-01"
LOT_NAME = "LOT-2026-001"
EXPECTED_QTY = 50.0


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
            f"agent likely failed to validate after assigning lot + quantity"
        )

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    lot = env["stock.lot"].search([
        ("name", "=", LOT_NAME),
        ("product_id", "=", product.id),
    ], limit=1)
    if not lot:
        failures.append(
            f"No stock.lot with name '{LOT_NAME}' for product "
            f"'{PRODUCT_NAME}' — agent did not enter the lot number"
        )

    # Confirm the move/move_line reflect the expected values
    if picking.state == "done":
        moves = picking.move_ids.filtered(lambda m: m.product_id.id == product.id)
        if not moves:
            failures.append(
                f"No stock.move for product '{PRODUCT_NAME}' on the receipt"
            )
        else:
            total_qty = sum(moves.mapped("quantity"))
            if abs(total_qty - EXPECTED_QTY) > 0.01:
                failures.append(
                    f"Total done quantity on move(s) is {total_qty}, "
                    f"expected {EXPECTED_QTY}"
                )

    # Quants: 50 units of the product should now be in WH/Stock on the target lot.
    stock_loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if stock_loc and picking.state == "done" and lot:
        quant = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", stock_loc.id),
            ("lot_id", "=", lot.id),
        ], limit=1)
        if not quant:
            failures.append(
                "No stock.quant in WH/Stock for the target lot after "
                "validation — receipt may have validated into a different "
                "location or lot"
            )
        elif abs(quant.quantity - EXPECTED_QTY) > 0.01:
            failures.append(
                f"Quant quantity is {quant.quantity}, expected {EXPECTED_QTY}"
            )

    return failures
