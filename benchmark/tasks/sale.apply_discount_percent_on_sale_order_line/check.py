"""Postcondition checks for sale.apply_discount_percent_on_sale_order_line.

Validates:
1. Products `Bench Product A` / `Bench Product B` and partner `Bench Disc Co`
   still exist.
2. Quotation `BENCH-DISC` still exists, state='draft', same customer,
   and exactly 2 order lines (no stray lines added or deleted).
3. The Bench Product A line still has qty=2 and now has discount == 10.0.
4. The Bench Product B line still has qty=3 and discount == 0.0 (unchanged).
5. Unit prices are untouched (A=50.0, B=20.0) and taxes are still cleared.
6. amount_untaxed reflects the discount:
      A subtotal = 2 * 50 * 0.9 = 90.0
      B subtotal = 3 * 20       = 60.0
      amount_untaxed           = 150.0
      amount_total             = 150.0 (no taxes)
"""

PARTNER_NAME = "Bench Disc Co"
SO_NAME = "BENCH-DISC"
PRODUCT_A = "Bench Product A"
PRODUCT_B = "Bench Product B"


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

    so = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)], limit=1
    )
    if not so:
        return [f"Quotation '{SO_NAME}' not found"]

    if so.partner_id.id != partner.id:
        failures.append(
            f"SO customer is '{so.partner_id.display_name}', expected '{PARTNER_NAME}'"
        )
    if so.state != "draft":
        failures.append(f"SO state is '{so.state}', expected 'draft'")

    lines = so.order_line
    if len(lines) != 2:
        failures.append(
            f"Expected exactly 2 order lines, found {len(lines)} "
            f"(products: {lines.mapped('product_id.name')})"
        )
        return failures

    by_product = {l.product_id.id: l for l in lines}

    # --- Line A: Bench Product A must have discount=10, qty=2, price=50 ---
    if product_a.id not in by_product:
        failures.append(f"Missing line for product '{PRODUCT_A}'")
    else:
        la = by_product[product_a.id]
        if abs(la.product_uom_qty - 2) > 0.001:
            failures.append(
                f"'{PRODUCT_A}' qty is {la.product_uom_qty}, expected 2"
            )
        if abs(la.price_unit - 50.0) > 0.01:
            failures.append(
                f"'{PRODUCT_A}' price_unit is {la.price_unit}, expected 50.0"
            )
        if abs(la.discount - 10.0) > 0.01:
            failures.append(
                f"'{PRODUCT_A}' discount is {la.discount}, expected 10.0 "
                f"(the task is to set the per-line Disc.% to 10% on this row)"
            )

    # --- Line B: Bench Product B must be UNTOUCHED (discount=0, qty=3, price=20) ---
    if product_b.id not in by_product:
        failures.append(f"Missing line for product '{PRODUCT_B}'")
    else:
        lb = by_product[product_b.id]
        if abs(lb.product_uom_qty - 3) > 0.001:
            failures.append(
                f"'{PRODUCT_B}' qty is {lb.product_uom_qty}, expected 3 (must not be modified)"
            )
        if abs(lb.price_unit - 20.0) > 0.01:
            failures.append(
                f"'{PRODUCT_B}' price_unit is {lb.price_unit}, expected 20.0 (must not be modified)"
            )
        if abs(lb.discount - 0.0) > 0.01:
            failures.append(
                f"'{PRODUCT_B}' discount is {lb.discount}, expected 0.0 "
                f"(discount should only have been applied to the first line)"
            )

    # --- amount_total must reflect the discount on line A only ---
    # Expected: 90 (A) + 60 (B) = 150.0 untaxed; no taxes → total 150.0
    if abs(so.amount_untaxed - 150.0) > 0.01:
        failures.append(
            f"SO amount_untaxed is {so.amount_untaxed}, expected 150.0 "
            f"(90 from A with 10% disc + 60 from B)"
        )
    if abs(so.amount_total - 150.0) > 0.01:
        failures.append(
            f"SO amount_total is {so.amount_total}, expected 150.0 "
            f"(no taxes → equals amount_untaxed)"
        )

    return failures
