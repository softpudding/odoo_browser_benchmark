"""Postconditions for stock.receive_lot_tracked_product."""

PRODUCT_NAME = "Apex Turbine Rotor"
RECEIPT_ORIGIN = "BENCH-LOT-RCV-01"
LOT_NAME = "LOT-2026-R042"


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
            f"agent likely failed to validate after assigning a lot"
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

    # Quants: 20 units of the product should now be in WH/Stock.
    stock_loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if stock_loc and picking.state == "done":
        quant = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", stock_loc.id),
            ("lot_id", "=", lot.id if lot else 0),
        ], limit=1)
        if not quant:
            failures.append(
                "No stock.quant in WH/Stock for the target lot after "
                "validation — receipt may have validated into a different "
                "location or lot"
            )
        elif quant.quantity != 20.0:
            failures.append(
                f"Quant quantity is {quant.quantity}, expected 20.0"
            )

    return failures
