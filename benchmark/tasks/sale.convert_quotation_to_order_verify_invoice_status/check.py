"""Postcondition checks for sale.convert_quotation_to_order_verify_invoice_status.

Validates:
1. Partner `Bench Confirm Co` and product `Bench Confirm Item` still exist.
2. Quotation `BENCH-CONFIRM` still exists and has state='sale' (confirmed).
3. Exactly 1 order line (Bench Confirm Item qty=1 price=100).
4. Exactly 1 sale.order row for Bench Confirm Co (no duplicates).
5. amount_untaxed = amount_total = 100.0 (no taxes).
"""

PARTNER_NAME = "Bench Confirm Co"
SO_NAME = "BENCH-CONFIRM"
PRODUCT_NAME = "Bench Confirm Item"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Customer '{PARTNER_NAME}' not found"]

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    # Exactly one SO for this customer (no duplicates created)
    partner_orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", partner.id)]
    )
    if len(partner_orders) != 1:
        failures.append(
            f"Expected exactly 1 sale.order for '{PARTNER_NAME}', "
            f"found {len(partner_orders)} (names: {partner_orders.mapped('name')})"
        )

    so = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)], limit=1
    )
    if not so:
        failures.append(f"Quotation '{SO_NAME}' not found")
        return failures

    if so.partner_id.id != partner.id:
        failures.append(
            f"SO customer is '{so.partner_id.display_name}', expected '{PARTNER_NAME}'"
        )
    if so.state != "sale":
        failures.append(
            f"SO state is '{so.state}', expected 'sale' (did you click Confirm?)"
        )

    lines = so.order_line
    if len(lines) != 1:
        failures.append(
            f"Expected exactly 1 order line, found {len(lines)} "
            f"(products: {lines.mapped('product_id.name')})"
        )
        return failures

    line = lines[0]
    if line.product_id.id != product.id:
        failures.append(
            f"Line product is '{line.product_id.display_name}', "
            f"expected '{PRODUCT_NAME}'"
        )
    if abs(line.product_uom_qty - 1) > 0.001:
        failures.append(
            f"Line qty is {line.product_uom_qty}, expected 1 (must not be modified)"
        )
    if abs(line.price_unit - 100.0) > 0.01:
        failures.append(
            f"Line price_unit is {line.price_unit}, expected 100.0 (must not be modified)"
        )

    if abs(so.amount_untaxed - 100.0) > 0.01:
        failures.append(
            f"SO amount_untaxed is {so.amount_untaxed}, expected 100.0"
        )
    if abs(so.amount_total - 100.0) > 0.01:
        failures.append(
            f"SO amount_total is {so.amount_total}, expected 100.0 (no taxes)"
        )

    return failures
