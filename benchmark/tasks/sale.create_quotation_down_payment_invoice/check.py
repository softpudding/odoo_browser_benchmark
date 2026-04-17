"""Postcondition checks for sale.create_quotation_down_payment_invoice.

Validates:
- SO exists, confirmed, with exact 2 product lines
- Customer ref is correct
- Down payment invoice exists, posted, with correct 30% amount
- Invoice date is correct
- No extra invoices
"""

from datetime import date


PARTNER_NAME = "Ridgeline Automation"
CLIENT_REF = "RA-DP-2026"
EXPECTED_LINES = {
    "Modular Conveyor Belt": {"product_uom_qty": 5.0, "price_unit": 1200.0},
    "Safety Light Curtain":  {"product_uom_qty": 10.0, "price_unit": 350.0},
}
# SO total = 5*1200 + 10*350 = 6000 + 3500 = 9500
# 30% down payment = 2850
SO_TOTAL = 9500.0
DOWN_PAYMENT_AMOUNT = 2850.0
DOWN_PAYMENT_PCT = 30.0


def check(env):
    failures = []

    # --- Partner ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    # --- Sales Order ---
    order = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", CLIENT_REF),
    ], limit=1)
    if not order:
        return [f"Sales order with ref '{CLIENT_REF}' not found"]

    if order.state != "sale":
        failures.append(f"SO state is '{order.state}', expected 'sale'")

    if order.client_order_ref != CLIENT_REF:
        failures.append(
            f"Customer ref is '{order.client_order_ref}', expected '{CLIENT_REF}'"
        )

    # --- Check SO lines ---
    product_lines = order.order_line.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
        and l.product_id
        and not l.is_downpayment
    )

    if len(product_lines) != 2:
        failures.append(
            f"Expected 2 product lines on SO, found {len(product_lines)} "
            f"(products: {[l.product_id.name for l in product_lines]})"
        )

    remaining = dict(EXPECTED_LINES)
    for line in product_lines:
        name = line.product_id.name
        if name not in remaining:
            failures.append(f"Unexpected product line on SO: {name}")
            continue
        exp = remaining.pop(name)
        if abs(line.product_uom_qty - exp["product_uom_qty"]) > 0.01:
            failures.append(
                f"{name} qty: expected {exp['product_uom_qty']}, got {line.product_uom_qty}"
            )
        if abs(line.price_unit - exp["price_unit"]) > 0.01:
            failures.append(
                f"{name} price: expected {exp['price_unit']}, got {line.price_unit}"
            )

    for missing in remaining:
        failures.append(f"Missing product line on SO: {missing}")

    # --- Check SO total (no taxes) ---
    if abs(order.amount_total - SO_TOTAL) > 0.01:
        failures.append(
            f"SO total is {order.amount_total}, expected {SO_TOTAL}"
        )

    # --- Check expiration date ---
    if order.validity_date and str(order.validity_date) != "2026-06-15":
        failures.append(
            f"Expiration date is '{order.validity_date}', expected '2026-06-15'"
        )

    # --- Down payment invoice ---
    invoices = order.invoice_ids.filtered(
        lambda m: m.move_type == "out_invoice"
    )
    if len(invoices) == 0:
        failures.append("No invoice found linked to the sales order")
        return failures

    if len(invoices) > 1:
        failures.append(
            f"Expected 1 invoice, found {len(invoices)} "
            f"(states: {[inv.state for inv in invoices]})"
        )

    invoice = invoices[0]

    if invoice.state != "posted":
        failures.append(f"Invoice state is '{invoice.state}', expected 'posted'")

    if invoice.invoice_date != date(2026, 6, 1):
        failures.append(
            f"Invoice date is {invoice.invoice_date}, expected 2026-06-01"
        )

    # --- Check invoice amount matches 30% down payment ---
    if abs(invoice.amount_total - DOWN_PAYMENT_AMOUNT) > 1.0:
        failures.append(
            f"Invoice total is {invoice.amount_total}, expected ~{DOWN_PAYMENT_AMOUNT} "
            f"(30% of {SO_TOTAL})"
        )

    # --- Ensure no other stray invoices for this partner ---
    all_invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
        ("id", "not in", invoices.ids),
    ])
    if all_invoices:
        failures.append(
            f"Found {len(all_invoices)} extra invoice(s) for this partner "
            f"(ids: {all_invoices.ids})"
        )

    return failures
