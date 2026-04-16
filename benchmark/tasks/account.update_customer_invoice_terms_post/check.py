"""Postcondition checks for account.update_customer_invoice_terms_post."""

from datetime import date


def _product_lines(invoice):
    return invoice.invoice_line_ids.filtered(
        lambda line: line.display_type == "product" or (not line.display_type and line.product_id)
    )


def check(env):
    failures = []

    invoice = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        ("invoice_origin", "=", "MED-CINV-01"),
    ], limit=1)
    if not invoice:
        return ["Target invoice 'MED-CINV-01' not found"]

    if invoice.partner_id.name != "Brightstar Labs":
        failures.append(
            f"Customer is '{invoice.partner_id.name}', expected 'Brightstar Labs'"
        )
    if invoice.state != "posted":
        failures.append(f"Invoice state is '{invoice.state}', expected 'posted'")
    if invoice.ref != "BRIGHT-READY":
        failures.append(f"Customer Reference is '{invoice.ref}', expected 'BRIGHT-READY'")
    if invoice.invoice_date != date(2026, 5, 14):
        failures.append(
            f"Invoice date is {invoice.invoice_date}, expected 2026-05-14"
        )
    if not invoice.invoice_payment_term_id:
        failures.append("Payment Terms not set")
    elif invoice.invoice_payment_term_id.name != "30 Net Days":
        failures.append(
            f"Payment Terms are '{invoice.invoice_payment_term_id.name}', expected '30 Net Days'"
        )

    lines = _product_lines(invoice)
    if len(lines) != 1:
        failures.append(f"Expected 1 product line, found {len(lines)}")
        return failures

    support = lines.filtered(lambda line: line.product_id.name == "Support Review")

    if not support:
        failures.append("Support Review line not found")
    else:
        if support.quantity != 4:
            failures.append(
                f"Support Review quantity is {support.quantity}, expected 4"
            )
        if support.price_unit != 450.0:
            failures.append(
                f"Support Review unit price is {support.price_unit}, expected 450.0"
            )

    distractor = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        ("invoice_origin", "=", "MED-CINV-02"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor invoice 'MED-CINV-02' not found")
    else:
        if distractor.state != "draft":
            failures.append(
                f"Distractor invoice state is '{distractor.state}', expected 'draft'"
            )
        if distractor.ref != "MED-CINV-02":
            failures.append(
                f"Distractor reference is '{distractor.ref}', expected 'MED-CINV-02'"
            )
        d_lines = _product_lines(distractor)
        d_support = d_lines.filtered(lambda line: line.product_id.name == "Support Review")
        if d_support and d_support.quantity != 3:
            failures.append(
                f"Distractor Support Review quantity is {d_support.quantity}, expected 3"
            )

    return failures
