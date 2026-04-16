"""Postcondition checks for sale.create_invoice_adjust_quantity_post."""

from datetime import date


PARTNER_NAME = "Northwind Studio"
TARGET_REF = "MED-INV-SO-01"
DISTRACTOR_REF = "MED-INV-SO-02"


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    order = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", TARGET_REF),
    ], limit=1)
    if not order:
        return [f"Sales order '{TARGET_REF}' not found"]

    if order.state != "sale":
        failures.append(f"Target order state is '{order.state}', expected 'sale'")
    if order.invoice_status != "invoiced":
        failures.append(
            f"Target order invoice status is '{order.invoice_status}', expected 'invoiced'"
        )

    invoices = order.invoice_ids.filtered(lambda move: move.move_type == "out_invoice")
    if len(invoices) != 1:
        failures.append(f"Expected 1 customer invoice, found {len(invoices)}")
        return failures

    invoice = invoices[0]
    if invoice.state != "posted":
        failures.append(f"Invoice state is '{invoice.state}', expected 'posted'")
    if invoice.invoice_date != date(2026, 5, 12):
        failures.append(
            f"Invoice date is {invoice.invoice_date}, expected 2026-05-12"
        )
    if not invoice.invoice_payment_term_id:
        failures.append("Invoice payment terms were not set")
    elif invoice.invoice_payment_term_id.name != "30 Net Days":
        failures.append(
            f"Invoice payment terms are '{invoice.invoice_payment_term_id.name}', expected '30 Net Days'"
        )

    lines = invoice.invoice_line_ids.filtered(
        lambda line: line.display_type == "product" or (not line.display_type and line.product_id)
    )
    if len(lines) != 2:
        failures.append(f"Expected 2 invoice lines, found {len(lines)}")
        return failures

    support = lines.filtered(lambda line: line.product_id.name == "Support Retainer")
    implementation = lines.filtered(
        lambda line: line.product_id.name == "Implementation Block"
    )

    if not support:
        failures.append("Support Retainer line not found")
    else:
        if support.quantity != 3:
            failures.append(
                f"Support Retainer quantity is {support.quantity}, expected 3"
            )
        if support.price_unit != 1500.0:
            failures.append(
                f"Support Retainer unit price is {support.price_unit}, expected 1500.0"
            )

    if not implementation:
        failures.append("Implementation Block line not found")
    else:
        if implementation.quantity != 1:
            failures.append(
                f"Implementation Block quantity is {implementation.quantity}, expected 1"
            )
        if implementation.price_unit != 2400.0:
            failures.append(
                f"Implementation Block unit price is {implementation.price_unit}, expected 2400.0"
            )

    distractor = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", DISTRACTOR_REF),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor order '{DISTRACTOR_REF}' not found")
    else:
        if distractor.invoice_ids.filtered(lambda move: move.move_type == "out_invoice"):
            failures.append("Distractor order was invoiced")

    return failures
