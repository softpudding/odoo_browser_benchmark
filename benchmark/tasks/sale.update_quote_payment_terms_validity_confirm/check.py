"""Postcondition checks for sale.update_quote_payment_terms_validity_confirm."""

from datetime import date


def check(env):
    failures = []
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        return ["Partner 'Azure Interior' not found"]
    so = env["sale.order"].search([("partner_id", "=", partner.id), ("client_order_ref", "=", "BENCH-PMT-02")], limit=1)
    if not so:
        return ["Sales order BENCH-PMT-02 not found"]
    if so.state != "sale":
        failures.append(f"Order state is '{so.state}', expected 'sale'")
    if not so.payment_term_id or so.payment_term_id.name != "30 Net Days":
        failures.append("Payment terms are not set to '30 Net Days'")
    if so.validity_date != date(2026, 5, 28):
        failures.append(f"Expiration date is {so.validity_date}, expected 2026-05-28")
    desk = so.order_line.filtered(lambda l: l.product_id.name == "Desk Organizer")
    if not desk:
        failures.append("Desk Organizer line not found")
    else:
        if desk.product_uom_qty != 12:
            failures.append(f"Desk Organizer qty is {desk.product_uom_qty}, expected 12")
        if desk.price_unit != 25.0:
            failures.append(f"Desk Organizer price is {desk.price_unit}, expected 25.0")
    return failures
