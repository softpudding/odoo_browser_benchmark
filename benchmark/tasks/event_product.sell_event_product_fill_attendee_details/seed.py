"""Seed for event_product.sell_event_product_fill_attendee_details."""


EVENT_NAME = "Partner Enablement Day"
PARTNER_NAME = "Northwind Workshops"
PARTNER_EMAIL = "orders@northwind-workshops.test"
PRODUCT_NAME = "Enablement Seat Product"
TICKET_NAME = "Workshop Seat"
ATTENDEE_NAME = "Jordan Rivera"


def _cleanup_invoices(env, partner):
    moves = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    for move in moves:
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


def _cleanup_orders(env, partner):
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


def _cleanup_event(env):
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if not events:
        return
    regs = env["event.registration"].with_context(active_test=False).search([
        ("event_id", "in", events.ids),
    ])
    if regs:
        regs.unlink()
    events.mapped("event_ticket_ids").unlink()
    events.unlink()


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "customer_rank": 1,
            "email": PARTNER_EMAIL,
        })
    else:
        partner.write({
            "is_company": True,
            "customer_rank": max(partner.customer_rank, 1),
            "email": PARTNER_EMAIL,
        })
    return partner


def _ensure_product(env):
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    vals = {
        "name": PRODUCT_NAME,
        "type": "service",
        "service_tracking": "event",
        "list_price": 95.0,
        "standard_price": 0.0,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    }
    if product:
        product.product_tmpl_id.write(vals)
        return product
    return env["product.template"].create(vals).product_variant_id


def setup(env):
    partner = _ensure_partner(env)
    _cleanup_invoices(env, partner)
    _cleanup_orders(env, partner)
    _cleanup_event(env)

    product = _ensure_product(env)
    event = env["event.event"].create({
        "name": EVENT_NAME,
        "date_begin": "2026-06-02 09:00:00",
        "date_end": "2026-06-02 17:00:00",
    })
    env["event.event.ticket"].create({
        "event_id": event.id,
        "name": TICKET_NAME,
        "price": 95.0,
        "seats_max": 40,
        "product_id": product.id,
    })

    env["event.registration"].search([("name", "=", ATTENDEE_NAME)]).unlink()
