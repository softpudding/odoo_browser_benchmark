"""Postcondition checks for sale.duplicate_quotation_edit_delivery_date_confirm.

Validates:
1. Products `Bench SO Item A` / `Bench SO Item B` and partner `Bench Copy Co`
   still exist.
2. Original quotation `S-BENCH-COPY-001` is unchanged — same customer,
   state='draft', exactly 2 lines (A qty=2, B qty=3), commitment_date unset.
3. A NEW sale.order exists for `Bench Copy Co` (the duplicate): state='sale',
   commitment_date date-part == 2026-08-15 (allowing admin-tz datetime
   conversion), exactly 2 order lines matching the seeded products and
   quantities.
4. Exactly 2 sale.order rows for Bench Copy Co across the whole run.
"""

from datetime import date, datetime, timedelta

PARTNER_NAME = "Bench Copy Co"
SOURCE_SO_NAME = "S-BENCH-COPY-001"
PRODUCT_A = "Bench SO Item A"
PRODUCT_B = "Bench SO Item B"
TARGET_DATE = date(2026, 8, 15)


def _assert_two_lines(order, product_a, product_b, failures, label):
    lines = order.order_line
    if len(lines) != 2:
        failures.append(
            f"{label}: expected 2 order_line rows, found {len(lines)}"
        )
        return
    by_product = {l.product_id.id: l for l in lines}
    if product_a.id not in by_product:
        failures.append(f"{label}: missing line for '{PRODUCT_A}'")
    elif abs(by_product[product_a.id].product_uom_qty - 2) > 0.001:
        failures.append(
            f"{label}: '{PRODUCT_A}' qty is {by_product[product_a.id].product_uom_qty}, expected 2"
        )
    if product_b.id not in by_product:
        failures.append(f"{label}: missing line for '{PRODUCT_B}'")
    elif abs(by_product[product_b.id].product_uom_qty - 3) > 0.001:
        failures.append(
            f"{label}: '{PRODUCT_B}' qty is {by_product[product_b.id].product_uom_qty}, expected 3"
        )


def _commitment_date_matches(value):
    """Accept either a datetime or a date. For datetimes, accept any
    instant whose date is TARGET_DATE in UTC OR (UTC + admin tz offset);
    admin default tz is UTC in benchmark_base, but allow up to ±24h to be
    generous about timezone conversions on the UI."""
    if not value:
        return False
    if isinstance(value, datetime):
        if value.date() == TARGET_DATE:
            return True
        # Allow tz drift of up to 1 day in either direction.
        for delta_hours in range(-24, 25):
            shifted = value + timedelta(hours=delta_hours)
            if shifted.date() == TARGET_DATE:
                return True
        return False
    if isinstance(value, date):
        return value == TARGET_DATE
    return False


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    product_a = env["product.product"].search([("name", "=", PRODUCT_A)], limit=1)
    product_b = env["product.product"].search([("name", "=", PRODUCT_B)], limit=1)
    if not product_a:
        return [f"Product '{PRODUCT_A}' not found"]
    if not product_b:
        return [f"Product '{PRODUCT_B}' not found"]

    # --- Original must still exist and be unchanged ---
    original = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SOURCE_SO_NAME)], limit=1
    )
    if not original:
        failures.append(
            f"Original quotation '{SOURCE_SO_NAME}' is missing"
        )
    else:
        if original.partner_id.id != partner.id:
            failures.append(
                f"Original customer is '{original.partner_id.display_name}', "
                f"expected '{PARTNER_NAME}'"
            )
        if original.state != "draft":
            failures.append(
                f"Original state is '{original.state}', expected 'draft'"
            )
        _assert_two_lines(original, product_a, product_b, failures, "Original")
        if original.commitment_date:
            failures.append(
                f"Original commitment_date should be empty, got "
                f"{original.commitment_date!r}"
            )

    # --- Find the duplicate: a different sale.order for the same partner ---
    partner_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", partner.id)]
    )
    duplicates = partner_orders.filtered(lambda o: o.name != SOURCE_SO_NAME)

    if not duplicates:
        failures.append(
            f"No duplicate sale.order found for '{PARTNER_NAME}' "
            f"(apart from the original {SOURCE_SO_NAME})"
        )
        return failures

    if len(duplicates) > 1:
        failures.append(
            f"Expected exactly 1 duplicate for '{PARTNER_NAME}', found "
            f"{len(duplicates)} (names: {duplicates.mapped('name')})"
        )

    dup = duplicates[0]

    if dup.state != "sale":
        failures.append(
            f"Duplicate state is '{dup.state}', expected 'sale' (confirmed)"
        )

    if not _commitment_date_matches(dup.commitment_date):
        failures.append(
            f"Duplicate commitment_date is {dup.commitment_date!r}, "
            f"expected a datetime/date whose date part is {TARGET_DATE}"
        )

    _assert_two_lines(dup, product_a, product_b, failures, "Duplicate")

    # --- Total rows tied to this partner ---
    if len(partner_orders) != 2:
        failures.append(
            f"Expected exactly 2 sale.order rows for '{PARTNER_NAME}', "
            f"found {len(partner_orders)}"
        )

    return failures
