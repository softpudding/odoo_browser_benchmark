"""Seed for event_sale.multi_ticket_checkout_two_attendees.

Category: closed_loop_cross_module (HARD).

Seeds:
  - Customer partner "Bench Summit Customer".
  - Two service products (service_tracking='event'):
      * "Bench Summit Early Bird Ticket" (list_price=180.0)
      * "Bench Summit VIP Ticket"        (list_price=420.0)
  - Event "Bench Summit 2026" (single day, 2026-07-10) with two
    paid ticket types:
      * "Early Bird" -> Early Bird product (price 180)
      * "VIP"        -> VIP product        (price 420)

Cleans up prior runs (registrations, sale orders, event, and residual
attendee-name rows) so the task is idempotent.
"""

EVENT_NAME = "Bench Summit 2026"

TICKET_EARLY = "Early Bird"
TICKET_VIP = "VIP"

PRODUCT_EARLY = "Bench Summit Early Bird Ticket"
PRODUCT_VIP = "Bench Summit VIP Ticket"

PRICE_EARLY = 180.0
PRICE_VIP = 420.0

PARTNER_NAME = "Bench Summit Customer"
PARTNER_EMAIL = "billing@bench-summit.example"

# Attendee strings referenced by prompt/check (the agent is expected
# to write these exact values on the generated registrations).
ATTENDEE_EARLY_NAME = "Alice Summit Attendee"
ATTENDEE_EARLY_EMAIL = "alice.summit@example.com"
ATTENDEE_VIP_NAME = "Bob Summit Attendee"
ATTENDEE_VIP_EMAIL = "bob.summit@example.com"


def _ensure_event_sale_installed(env):
    """event_product + event_sale allow service products to drive
    ticket registrations through the sale workflow."""
    for mod_name in ("event_product", "event_sale"):
        module = env["ir.module.module"].search(
            [("name", "=", mod_name)], limit=1
        )
        if module and module.state != "installed":
            module.button_immediate_install()


def _cleanup_orders(env, partner):
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


def _cleanup_event(env):
    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if not events:
        return
    regs = env["event.registration"].search(
        [("event_id", "in", events.ids)]
    )
    if regs:
        try:
            regs.unlink()
        except Exception:
            pass
    try:
        events.mapped("event_ticket_ids").unlink()
    except Exception:
        pass
    try:
        events.unlink()
    except Exception:
        pass


def _cleanup_extra_registrations(env):
    env["event.registration"].search([
        ("name", "in", [ATTENDEE_EARLY_NAME, ATTENDEE_VIP_NAME]),
    ]).unlink()


def _ensure_partner(env):
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    vals = {
        "name": PARTNER_NAME,
        "is_company": True,
        "customer_rank": 1,
        "email": PARTNER_EMAIL,
    }
    if not partner:
        partner = env["res.partner"].create(vals)
    else:
        partner.write({
            "is_company": True,
            "customer_rank": max(partner.customer_rank, 1),
            "email": partner.email or PARTNER_EMAIL,
        })
    return partner


def _ensure_product(env, name, price):
    product = env["product.product"].search(
        [("name", "=", name)], limit=1
    )
    tmpl_vals = {
        "name": name,
        "type": "service",
        "service_tracking": "event",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": price,
        "standard_price": 0.0,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],  # Clear taxes for clean math.
        "supplier_taxes_id": [(5, 0, 0)],
    }
    if product:
        product.product_tmpl_id.write(tmpl_vals)
        return product
    tmpl = env["product.template"].create(tmpl_vals)
    return tmpl.product_variant_id


def setup(env):
    _ensure_event_sale_installed(env)

    partner = _ensure_partner(env)
    _cleanup_orders(env, partner)
    _cleanup_extra_registrations(env)
    _cleanup_event(env)

    early_product = _ensure_product(env, PRODUCT_EARLY, PRICE_EARLY)
    vip_product = _ensure_product(env, PRODUCT_VIP, PRICE_VIP)

    # Create the event with two distinct ticket types, each linked to
    # its own product.
    env["event.event"].create({
        "name": EVENT_NAME,
        "date_begin": "2026-07-10 09:00:00",
        "date_end": "2026-07-10 18:00:00",
        "event_ticket_ids": [
            (0, 0, {
                "name": TICKET_EARLY,
                "product_id": early_product.id,
                "price": PRICE_EARLY,
                "seats_max": 200,
            }),
            (0, 0, {
                "name": TICKET_VIP,
                "product_id": vip_product.id,
                "price": PRICE_VIP,
                "seats_max": 50,
            }),
        ],
    })
