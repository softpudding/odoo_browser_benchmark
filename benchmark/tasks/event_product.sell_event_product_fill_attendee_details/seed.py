"""Seed for event_product.sell_event_product_fill_attendee_details.

Category: closed_loop_cross_module (MEDIUM).

Seeds:
  - Customer partner "Bench Attendee Co".
  - Service product "Bench Summit Ticket" (service_tracking='event',
    list_price=100, invoice_policy='order'). The service_tracking
    'event' option is what materialises `event_ok=True` on the product
    variant so the SO line triggers the event configurator wizard.
  - Event "Bench Summit" with one paid ticket "Standard Pass" linked
    to the Bench Summit Ticket product (price=100). The auto-default
    "Registration for ..." ticket is pre-seeded with the built-in
    EVENT_REG product so the post-run diff does not emit a spurious
    ticket create for it.

Cleans up prior runs (registrations on Bench Summit or with the
Alice Attendee name, any sale.orders of Bench Attendee Co, the event
with its tickets, and any stale Bench Summit Ticket product).
"""

EVENT_NAME = "Bench Summit"
PARTNER_NAME = "Bench Attendee Co"
PARTNER_EMAIL = "billing@bench.test"
PRODUCT_NAME = "Bench Summit Ticket"
TICKET_NAME = "Standard Pass"
TICKET_PRICE = 100.0
ATTENDEE_NAME = "Alice Attendee"
ATTENDEE_EMAIL = "alice@bench.test"


def _cleanup_orders(env, partner):
    orders = env["sale.order"].with_context(active_test=False).search(
        [("partner_id", "=", partner.id)]
    )
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


def _cleanup_extra_registrations(env):
    regs = env["event.registration"].with_context(active_test=False).search(
        [("name", "=", ATTENDEE_NAME)]
    )
    if regs:
        regs.unlink()


def _cleanup_event(env):
    events = env["event.event"].with_context(active_test=False).search(
        [("name", "=", EVENT_NAME)]
    )
    if not events:
        return
    regs = env["event.registration"].with_context(active_test=False).search(
        [("event_id", "in", events.ids)]
    )
    if regs:
        regs.unlink()
    events.mapped("event_ticket_ids").unlink()
    events.unlink()


def _cleanup_product(env):
    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if not products:
        return
    # Cleanup tickets/registrations first, otherwise FK blocks unlink.
    tickets = env["event.event.ticket"].with_context(active_test=False).search(
        [("product_id", "in", products.ids)]
    )
    if tickets:
        regs = env["event.registration"].with_context(active_test=False).search(
            [("event_ticket_id", "in", tickets.ids)]
        )
        if regs:
            regs.unlink()
        tickets.unlink()
    templates = products.mapped("product_tmpl_id")
    try:
        products.unlink()
    except Exception:
        pass
    try:
        templates.unlink()
    except Exception:
        pass


def _ensure_partner(env):
    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
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
        "list_price": TICKET_PRICE,
        "standard_price": 0.0,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    }
    if product:
        product.product_tmpl_id.write(tmpl_vals)
        return product
    tmpl = env["product.template"].create(tmpl_vals)
    return tmpl.product_variant_id


def setup(env):
    partner = _ensure_partner(env)

    # Cleanup order matters: child -> parent.
    _cleanup_orders(env, partner)
    _cleanup_extra_registrations(env)
    _cleanup_event(env)
    _cleanup_product(env)

    product = _ensure_product(env)

    # Pre-seed the auto-default "Registration for ..." ticket so the
    # post-run diff only reflects the agent's actions (the SO line +
    # registration). We populate it with the built-in EVENT_REG product.
    default_product = env["product.product"].search(
        [("default_code", "=", "EVENT_REG")], limit=1
    )
    if not default_product:
        default_product = env.ref(
            "event_product.product_product_event", raise_if_not_found=False
        )

    ticket_lines = []
    if default_product:
        ticket_lines.append((0, 0, {
            "name": f"Registration for {EVENT_NAME}",
            "product_id": default_product.id,
        }))
    # The paid ticket the agent will actually sell.
    ticket_lines.append((0, 0, {
        "name": TICKET_NAME,
        "product_id": product.id,
        "price": TICKET_PRICE,
    }))

    env["event.event"].create({
        "name": EVENT_NAME,
        "date_begin": "2026-05-18 09:00:00",
        "date_end": "2026-05-19 17:00:00",
        "event_ticket_ids": ticket_lines,
    })
