"""Cleanup for event_product.sell_event_product_fill_attendee_details."""


EVENT_NAME = "Partner Enablement Day"
PARTNER_NAME = "Northwind Workshops"
ATTENDEE_NAME = "Jordan Rivera"


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ]).unlink()
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
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

    event = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ], limit=1)
    if event:
        env["event.registration"].with_context(active_test=False).search([
            ("event_id", "=", event.id),
        ]).unlink()
    env["event.registration"].search([("name", "=", ATTENDEE_NAME)]).unlink()
