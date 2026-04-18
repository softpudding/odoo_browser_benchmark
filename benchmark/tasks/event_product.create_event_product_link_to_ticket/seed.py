"""Seed for event_product.create_event_product_link_to_ticket.

Category: closed_loop_cross_module (MEDIUM).

Seeds:
  - Event "Spring Summit" with NO non-default ticket types (we
    pre-seed the auto-default 'Registration for ...' ticket so the
    diff captured during the run only reflects the ticket the agent
    adds).

Cleans up:
  - Any prior 'Conference Pass Std' product variants/templates.
  - Any prior 'Spring Summit' events including their tickets and
    registrations.
"""

EVENT_NAME = "Spring Summit"
PRODUCT_NAME = "Conference Pass Std"


def _cleanup_product(env):
    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if products:
        # Drop any tickets linked to this product to avoid FK problems.
        tickets = env["event.event.ticket"].with_context(
            active_test=False
        ).search([("product_id", "in", products.ids)])
        if tickets:
            regs = env["event.registration"].with_context(
                active_test=False
            ).search([("event_ticket_id", "in", tickets.ids)])
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


def setup(env):
    # Clean up tickets/products first (tickets reference the product).
    _cleanup_event(env)
    _cleanup_product(env)

    # Pre-seed the placeholder 'Registration for ...' ticket so the
    # auto-materialised default doesn't pollute the diff captured for
    # the agent's new ticket.
    default_product = env["product.product"].search(
        [("default_code", "=", "EVENT_REG")], limit=1
    )
    if not default_product:
        default_product = env.ref(
            "event_product.product_product_event", raise_if_not_found=False
        )

    event_vals = {
        "name": EVENT_NAME,
        "date_begin": "2026-05-20 09:00:00",
        "date_end": "2026-05-21 17:00:00",
    }
    if default_product:
        event_vals["event_ticket_ids"] = [(0, 0, {
            "name": f"Registration for {EVENT_NAME}",
            "product_id": default_product.id,
        })]
    env["event.event"].create(event_vals)
