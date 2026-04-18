"""Postconditions for product_expiry.receive_lot_set_expiry_date.

Verifies:
  - receipt BENCH-PERISH-RCV-01 is done
  - lot BP-LOT-001 exists for Bench Perishable
  - lot has explicit expiration_date near today+60d and removal_date
    near today+55d (the 30-day template default would be today+30, so
    we require the explicit override to land well above that)
  - 10 units of the product are quants in WH/Stock tied to the lot.
"""

from datetime import datetime, timedelta

PRODUCT_NAME = "Bench Perishable"
RECEIPT_ORIGIN = "BENCH-PERISH-RCV-01"
LOT_NAME = "BP-LOT-001"

EXPIRY_TARGET_DAYS = 60
REMOVAL_TARGET_DAYS = 55
DAY_TOLERANCE = 2


def _days_from_now(dt):
    if not dt:
        return None
    now = datetime.now()
    # Strip the time-of-day contribution so "today+60 at 00:00" doesn't
    # fail by a few hours either way.
    delta = (dt.date() - now.date()).days
    return delta


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
            f"agent likely failed to validate after creating the lot"
        )

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    if not product.product_tmpl_id.use_expiration_date:
        failures.append(
            "Product template lost use_expiration_date — seed drift"
        )

    lot = env["stock.lot"].search([
        ("name", "=", LOT_NAME),
        ("product_id", "=", product.id),
    ], limit=1)
    if not lot:
        failures.append(
            f"No stock.lot with name '{LOT_NAME}' for product "
            f"'{PRODUCT_NAME}' — agent did not create the lot"
        )
        return failures

    # Expiration date must be set and roughly today+60.
    if not lot.expiration_date:
        failures.append(
            "stock.lot.expiration_date is empty — agent did not open "
            "the lot form to set an explicit expiration date"
        )
    else:
        delta = _days_from_now(lot.expiration_date)
        if delta is None or abs(delta - EXPIRY_TARGET_DAYS) > DAY_TOLERANCE:
            failures.append(
                f"stock.lot.expiration_date is "
                f"{lot.expiration_date} (≈ {delta} days from today), "
                f"expected ≈ today+{EXPIRY_TARGET_DAYS} (±{DAY_TOLERANCE}). "
                f"Agent likely left the 30-day template default."
            )

    if not lot.removal_date:
        failures.append(
            "stock.lot.removal_date is empty — agent did not set an "
            "explicit removal date on the lot form"
        )
    else:
        delta = _days_from_now(lot.removal_date)
        if delta is None or abs(delta - REMOVAL_TARGET_DAYS) > DAY_TOLERANCE:
            failures.append(
                f"stock.lot.removal_date is "
                f"{lot.removal_date} (≈ {delta} days from today), "
                f"expected ≈ today+{REMOVAL_TARGET_DAYS} "
                f"(±{DAY_TOLERANCE})."
            )

    # use_date (Best before) should be populated automatically by the
    # product_expiry compute when expiration_date is set. We don't
    # require a specific value here, just non-null as a signal that
    # expiration_date was really written.
    if lot and lot.expiration_date and not lot.use_date:
        failures.append(
            "stock.lot.use_date is empty despite expiration_date being "
            "set — compute side-effect missing (unexpected)"
        )

    # Quants: 10 units of the product should be in WH/Stock on this lot.
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
                "No stock.quant in WH/Stock for the BP-LOT-001 lot "
                "after validation — receipt may have validated into a "
                "different location or lot"
            )
        elif quant.quantity != 10.0:
            failures.append(
                f"Quant quantity is {quant.quantity}, expected 10.0"
            )

    return failures
