"""Seed for event_sale.configure_paid_ticket_register_with_invoice.

Category: closed_loop_cross_module (HARD).

Seeds:
  - Event "Spring Dev Summit 2026" with NO ticket types yet.
  - Customer partner "Bench Summit Attendee Inc".
  - Service product "Dev Summit Pro Product" (service_tracking='event',
    list_price=150, invoice_policy='order') so the agent can pick it
    when creating the ticket and the SO line.

Cleans up prior runs (registrations, sale orders, invoices, the event,
and the partner's residual records) so the task is idempotent.
"""

EVENT_NAME = "Spring Dev Summit 2026"
PARTNER_NAME = "Bench Summit Attendee Inc"
PARTNER_EMAIL = "billing@benchsummit.test"
PRODUCT_NAME = "Dev Summit Pro Product"
ATTENDEE_NAME = "Berta Attendee"
ATTENDEE_EMAIL = "berta@benchsummit.test"


def _ensure_event_sale_installed(env):
    module = env["ir.module.module"].search(
        [("name", "=", "event_sale")], limit=1
    )
    if module and module.state != "installed":
        module.button_immediate_install()


def _cleanup_invoices(env, partner):
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
        if move.state in ("draft", "cancel"):
            try:
                move.button_cancel()
            except Exception:
                pass
        try:
            move.unlink()
        except Exception:
            pass


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
        regs.unlink()
    events.mapped("event_ticket_ids").unlink()
    events.unlink()


def _cleanup_extra_registrations(env):
    # Catch registrations on other events with our attendee name.
    env["event.registration"].search(
        [("name", "=", ATTENDEE_NAME)]
    ).unlink()


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
        "list_price": 150.0,
        "standard_price": 0.0,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],  # Clear customer taxes for clean math.
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
    _cleanup_invoices(env, partner)
    _cleanup_orders(env, partner)
    _cleanup_extra_registrations(env)
    _cleanup_event(env)

    # Seed the product the agent will use both on the ticket and on the SO line.
    _ensure_product(env)

    # Create the event. Pre-seed the auto-default "Registration for ..."
    # ticket Odoo materializes when an event form is opened, so that the
    # diff captured during the run only reflects the agent's own ticket.
    default_product = env["product.product"].search(
        [("default_code", "=", "EVENT_REG")], limit=1
    )
    if not default_product:
        default_product = env.ref(
            "event_product.product_product_event", raise_if_not_found=False
        )
    event_vals = {
        "name": EVENT_NAME,
        "date_begin": "2026-04-21 09:00:00",
        "date_end": "2026-04-22 17:00:00",
    }
    if default_product:
        event_vals["event_ticket_ids"] = [(0, 0, {
            "name": f"Registration for {EVENT_NAME}",
            "product_id": default_product.id,
        })]
    env["event.event"].create(event_vals)
