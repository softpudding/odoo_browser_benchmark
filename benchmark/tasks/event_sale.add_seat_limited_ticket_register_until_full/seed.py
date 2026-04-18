"""Seed for event_sale.add_seat_limited_ticket_register_until_full.

Category: deep_ui_interaction (MEDIUM).

Seeds:
  - Event "Spring Q2 Workshop" with NO ticket types yet (the agent
    must add the VIP Seat ticket itself).

Cleans up:
  - Any prior VIP-N registrations from previous runs.
  - Any prior 'Spring Q2 Workshop' event including its tickets and
    registrations.

The event_sale module is auto-installed when both event and sale are
present, but we still gate-install it for safety because the task
file is named with the event_sale prefix.
"""

EVENT_NAME = "Spring Q2 Workshop"
ATTENDEE_NAMES = [f"VIP-{i}" for i in range(1, 7)]  # VIP-1..VIP-6


def _ensure_event_sale_installed(env):
    module = env["ir.module.module"].search(
        [("name", "=", "event_sale")], limit=1
    )
    if module and module.state != "installed":
        module.button_immediate_install()


def _cleanup_attendees(env):
    # Remove every prior registration whose name matches our VIP-N
    # pattern (regardless of which event), to keep the slate clean
    # across re-runs.
    regs = env["event.registration"].with_context(active_test=False).search(
        [("name", "in", ATTENDEE_NAMES)]
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


def setup(env):
    _ensure_event_sale_installed(env)

    _cleanup_attendees(env)
    _cleanup_event(env)

    # Create the event with NO ticket types. Odoo can auto-materialize
    # a default "Registration for ..." ticket when the event form is
    # opened — to make the diff stable, pre-seed that placeholder
    # ticket here so any later diff only reflects the VIP Seat the
    # agent adds.
    default_product = env["product.product"].search(
        [("default_code", "=", "EVENT_REG")], limit=1
    )
    if not default_product:
        default_product = env.ref(
            "event_product.product_product_event", raise_if_not_found=False
        )

    event_vals = {
        "name": EVENT_NAME,
        "date_begin": "2026-05-12 09:00:00",
        "date_end": "2026-05-12 17:00:00",
    }
    if default_product:
        event_vals["event_ticket_ids"] = [(0, 0, {
            "name": f"Registration for {EVENT_NAME}",
            "product_id": default_product.id,
        })]
    env["event.event"].create(event_vals)
