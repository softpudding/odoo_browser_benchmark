"""Seed for event_sale.multi_ticket_checkout_two_attendees.

Category: closed-loop cross-module (back-office event config -> public
portal ticket purchase flow with multi-attendee form and non-default
payment method).

Creates a published event 'Bench Expo 2026' with TWO paid ticket types
(Standard 50, VIP 150). The agent must register TWO attendees (1x
Standard + 1x VIP) with distinct name/email rows, go through the
/shop/checkout + /shop/payment flow, and pay via Wire Transfer
(non-default: transfer provider is disabled by default in the base
snapshot, so the seed enables it explicitly).

Seed installs the bridge modules needed for the website_event_sale
flow (website_event_sale, payment_custom) and activates the
Wire Transfer payment provider in production state.

Cleanup is child-first (payment.transaction -> account.move ->
sale.order.line -> sale.order -> event.registration -> event.event)
so the task is idempotent across re-runs.
"""

EVENT_NAME = "Bench Expo 2026"
TICKET_STANDARD = "Standard"
TICKET_VIP = "VIP"
PRICE_STANDARD = 50.0
PRICE_VIP = 150.0

PRODUCT_STANDARD = "Bench Expo Standard Pass"
PRODUCT_VIP = "Bench Expo VIP Pass"

ATTENDEE_STANDARD_NAME = "Alice Standard"
ATTENDEE_STANDARD_EMAIL = "alice@benchexpo.test"
ATTENDEE_VIP_NAME = "Bob VIP"
ATTENDEE_VIP_EMAIL = "bob@benchexpo.test"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    tmpl_vals = {
        "name": name,
        "type": "service",
        "service_tracking": "event",
        "list_price": price,
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


def _cleanup_prior_runs(env):
    # Find any prior event(s)
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])

    # Find any prior sale.orders linked to these events' tickets or
    # to registrations with our attendees.
    attendee_emails = [ATTENDEE_STANDARD_EMAIL, ATTENDEE_VIP_EMAIL]
    attendee_names = [ATTENDEE_STANDARD_NAME, ATTENDEE_VIP_NAME]

    regs = env["event.registration"].with_context(active_test=False).search([
        "|", "|",
        ("event_id", "in", events.ids),
        ("email", "in", attendee_emails),
        ("name", "in", attendee_names),
    ])
    order_ids = set(regs.mapped("sale_order_id").ids)
    # Also pick up orders that carry our ticket products in case the
    # registration record was already deleted.
    products = env["product.product"].with_context(active_test=False).search([
        ("name", "in", [PRODUCT_STANDARD, PRODUCT_VIP]),
    ])
    if products:
        more_orders = env["sale.order"].with_context(active_test=False).search([
            ("order_line.product_id", "in", products.ids),
        ])
        order_ids.update(more_orders.ids)

    if order_ids:
        orders = env["sale.order"].with_context(active_test=False).browse(list(order_ids)).exists()
        # Cancel then delete the orders (and their invoices/payments).
        for order in orders:
            # Delete payment transactions first.
            txs = env["payment.transaction"].search([("sale_order_ids", "in", order.id)])
            for tx in txs:
                try:
                    tx.sudo().unlink()
                except Exception:
                    pass
            # Delete related invoices.
            moves = order.invoice_ids
            for move in moves:
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
                    order.with_context(disable_cancel_warning=True)._action_cancel()
                except Exception:
                    try:
                        order.action_cancel()
                    except Exception:
                        pass
            try:
                order.sudo().unlink()
            except Exception:
                pass

    # Remove any dangling registrations
    regs = env["event.registration"].with_context(active_test=False).search([
        "|", "|",
        ("event_id", "in", events.ids),
        ("email", "in", attendee_emails),
        ("name", "in", attendee_names),
    ])
    if regs:
        regs.sudo().unlink()

    # Remove events (tickets cascade)
    if events:
        events.mapped("event_ticket_ids").sudo().unlink()
        events.sudo().unlink()


def _enable_wire_transfer(env):
    """Enable the Wire Transfer custom provider for the current website."""
    provider = env.ref(
        "payment.payment_provider_transfer", raise_if_not_found=False
    )
    if not provider:
        return
    vals = {"state": "enabled", "is_published": True}
    # Try to attach provider to the main company/website.
    provider.write(vals)
    # Make sure transfer has a pending message / at least one payment method
    # (the default data installs this already, so a no-op otherwise).


def _disable_competing_providers(env):
    """Leave Wire Transfer as the ONLY enabled provider so the payment
    step is deterministic. The base snapshot typically only has the
    demo 'Demo' (custom) provider enabled; disable everything that's
    not 'payment_provider_transfer'."""
    transfer = env.ref("payment.payment_provider_transfer", raise_if_not_found=False)
    others = env["payment.provider"].search([
        ("state", "in", ("enabled", "test")),
    ])
    for provider in others:
        if transfer and provider.id == transfer.id:
            continue
        try:
            provider.write({"state": "disabled"})
        except Exception:
            pass


def _ensure_admin_address(env):
    """Give admin's partner a complete billing/shipping address so the
    /shop/address step can be auto-skipped (try_skip_step=true) during
    checkout.  For US (state_required=True, zip_required=True) we need
    street/city/zip/state_id/country_id AND phone/email/name.
    """
    admin = env.ref("base.user_admin")
    partner = admin.partner_id

    updates = {}
    us = env.ref("base.us")
    ca_state = env.ref("base.state_us_5")  # California
    if not partner.country_id:
        updates["country_id"] = us.id
    if not partner.state_id:
        # Only set if country requires it.
        updates["state_id"] = ca_state.id
    if not partner.street:
        updates["street"] = "1 Bench Way"
    if not partner.city:
        updates["city"] = "San Francisco"
    if not partner.zip:
        updates["zip"] = "94105"
    if not partner.phone:
        updates["phone"] = "+1 555 0100"
    if not partner.email:
        updates["email"] = "admin@benchexpo.test"
    if updates:
        partner.write(updates)


def setup(env):
    # ----- 1. Install required modules -----
    _ensure_module(env, "website_event")
    _ensure_module(env, "website_event_sale")
    _ensure_module(env, "payment_custom")

    # Defer payment-confirmation mails so a missing SMTP provider in
    # the ephemeral test DB does NOT roll back the
    # payment_transaction._post_process() cursor, which would otherwise
    # leave the SO stuck in `draft` (no `action_quotation_sent`).
    env["ir.config_parameter"].sudo().set_param("sale.async_emails", "True")

    # ----- 2. Cleanup prior runs -----
    _cleanup_prior_runs(env)

    # ----- 3. Enable Wire Transfer as the only payment provider -----
    _enable_wire_transfer(env)
    _disable_competing_providers(env)

    # ----- 4. Ensure admin has an address so /shop/address can skip -----
    _ensure_admin_address(env)

    # ----- 5. Seed products -----
    product_std = _ensure_product(env, PRODUCT_STANDARD, PRICE_STANDARD)
    product_vip = _ensure_product(env, PRODUCT_VIP, PRICE_VIP)

    # ----- 6. Create the event with two published tickets -----
    event_vals = {
        "name": EVENT_NAME,
        "date_begin": "2026-09-10 09:00:00",
        "date_end": "2026-09-11 17:00:00",
        "event_ticket_ids": [
            (0, 0, {
                "name": TICKET_STANDARD,
                "product_id": product_std.id,
                "price": PRICE_STANDARD,
                "seats_max": 0,  # unlimited
            }),
            (0, 0, {
                "name": TICKET_VIP,
                "product_id": product_vip.id,
                "price": PRICE_VIP,
                "seats_max": 0,
            }),
        ],
    }
    event = env["event.event"].create(event_vals)

    # Publish on the website so /event and /event/<slug>/register work.
    if "is_published" in event._fields:
        event.write({"is_published": True})
    if "website_published" in event._fields:
        event.write({"website_published": True})
