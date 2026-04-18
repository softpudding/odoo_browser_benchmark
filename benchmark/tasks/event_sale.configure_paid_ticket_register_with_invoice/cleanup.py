"""Cleanup for event_sale.configure_paid_ticket_register_with_invoice."""

EVENT_NAME = "Spring Dev Summit 2026"
PARTNER_NAME = "Bench Summit Attendee Inc"
PRODUCT_NAME = "Dev Summit Pro Product"
ATTENDEE_NAME = "Berta Attendee"


def cleanup(env):
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        moves = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ])
        for move in moves:
            for payment in move._get_reconciled_payments():
                if payment.state == "posted":
                    payment.action_draft()
                payment.unlink()
            if move.state == "posted":
                move.button_draft()
            try:
                move.button_cancel()
            except Exception:
                pass
            try:
                move.unlink()
            except Exception:
                pass

        orders = env["sale.order"].search([("partner_id", "=", partner.id)])
        for order in orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            try:
                order.unlink()
            except Exception:
                pass

    env["event.registration"].search(
        [("name", "=", ATTENDEE_NAME)]
    ).unlink()

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if events:
        events.mapped("event_ticket_ids").unlink()
        events.unlink()
