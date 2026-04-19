"""Seed for event_product.sell_event_product_fill_attendee_details.

Category: closed_loop_cross_module (MEDIUM).

Seeds:
  - Customer partner "Bench Attendee Customer".
  - Service product "Bench Standard Ticket" (service_tracking='event',
    sale_ok=True, list_price=120) that acts as the ticket product.
  - Event "Bench Festival 2026" (single day, 2026-06-15) with a single
    ticket type "Standard" whose product_id is the Bench Standard Ticket.

Cleans up prior runs (registrations, sale orders, event, and the
partner's residual records) so the task is idempotent.
"""

EVENT_NAME = "Bench Festival 2026"
TICKET_NAME = "Standard"
PRODUCT_NAME = "Bench Standard Ticket"
PARTNER_NAME = "Bench Attendee Customer"
PARTNER_EMAIL = "billing@bench-attendee.example"

# Attendee strings referenced by prompt/check (the agent is expected to
# write these exact values on the generated registration).
ATTENDEE_NAME = "Bench Attendee Name"
ATTENDEE_EMAIL = "bench.attendee@example.com"


def _ensure_event_sale_installed(env):
    """event_product + event_sale allow a service product to drive
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
    # Catch registrations with our attendee name on any event.
    env["event.registration"].search(
        [("name", "=", ATTENDEE_NAME)]
    ).unlink()


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


def _ensure_product(env):
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    tmpl_vals = {
        "name": PRODUCT_NAME,
        "type": "service",
        "service_tracking": "event",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 120.0,
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

    product = _ensure_product(env)

    # Create the event with exactly one ticket type "Standard" linked
    # to the bench product.
    env["event.event"].create({
        "name": EVENT_NAME,
        "date_begin": "2026-06-15 09:00:00",
        "date_end": "2026-06-15 17:00:00",
        "event_ticket_ids": [(0, 0, {
            "name": TICKET_NAME,
            "product_id": product.id,
            "price": 120.0,
            "seats_max": 100,
        })],
    })
