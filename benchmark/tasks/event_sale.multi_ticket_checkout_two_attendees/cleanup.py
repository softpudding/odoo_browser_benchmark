"""Cleanup for event_sale.multi_ticket_checkout_two_attendees."""

EVENT_NAME = "Bench Expo 2026"
PRODUCT_STANDARD = "Bench Expo Standard Pass"
PRODUCT_VIP = "Bench Expo VIP Pass"
ATTENDEE_STANDARD_NAME = "Alice Standard"
ATTENDEE_STANDARD_EMAIL = "alice@benchexpo.test"
ATTENDEE_VIP_NAME = "Bob VIP"
ATTENDEE_VIP_EMAIL = "bob@benchexpo.test"


def cleanup(env):
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    products = env["product.product"].with_context(active_test=False).search([
        ("name", "in", [PRODUCT_STANDARD, PRODUCT_VIP]),
    ])

    # Collect related sale orders.
    regs = env["event.registration"].with_context(active_test=False).search([
        "|", "|",
        ("event_id", "in", events.ids),
        ("email", "in", [ATTENDEE_STANDARD_EMAIL, ATTENDEE_VIP_EMAIL]),
        ("name", "in", [ATTENDEE_STANDARD_NAME, ATTENDEE_VIP_NAME]),
    ])
    order_ids = set(regs.mapped("sale_order_id").ids)
    if products:
        more = env["sale.order"].with_context(active_test=False).search([
            ("order_line.product_id", "in", products.ids),
        ])
        order_ids.update(more.ids)

    if order_ids:
        orders = env["sale.order"].with_context(active_test=False).browse(list(order_ids)).exists()
        for order in orders:
            txs = env["payment.transaction"].search([
                ("sale_order_ids", "in", order.id)
            ])
            for tx in txs:
                try:
                    tx.sudo().unlink()
                except Exception:
                    pass
            for move in order.invoice_ids:
                if move.state == "posted":
                    try:
                        move.button_draft()
                    except Exception:
                        pass
                try:
                    move.button_cancel()
                except Exception:
                    pass
                try:
                    move.sudo().unlink()
                except Exception:
                    pass
            if order.state in ("sale", "done"):
                try:
                    order._action_cancel()
                except Exception:
                    try:
                        order.action_cancel()
                    except Exception:
                        pass
            try:
                order.sudo().unlink()
            except Exception:
                pass

    regs = env["event.registration"].with_context(active_test=False).search([
        "|", "|",
        ("event_id", "in", events.ids),
        ("email", "in", [ATTENDEE_STANDARD_EMAIL, ATTENDEE_VIP_EMAIL]),
        ("name", "in", [ATTENDEE_STANDARD_NAME, ATTENDEE_VIP_NAME]),
    ])
    if regs:
        regs.sudo().unlink()

    if events:
        events.mapped("event_ticket_ids").sudo().unlink()
        events.sudo().unlink()

    if products:
        # Product templates too, to avoid name conflicts on next seed.
        tmpls = products.mapped("product_tmpl_id")
        try:
            products.sudo().unlink()
        except Exception:
            pass
        try:
            tmpls.sudo().unlink()
        except Exception:
            pass
