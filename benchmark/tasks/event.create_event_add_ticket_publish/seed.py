"""Seed for event.create_event_add_ticket_publish.

Category: deep_ui_interaction (MEDIUM).

This task is a pure create-from-scratch event flow: the agent must
create a brand-new event, attach a single ticket type with an exact
price, and flip the website Published switch.

The seed only cleans up prior-run artefacts (event + any tickets/
registrations) so reruns are idempotent. The event module is part of
the benchmark base, so no module install is required; however
`website_event` must be installed for the `is_published` / Publish
switch to be functional, so we install it defensively.
"""


EVENT_NAME = "Bench Summer Summit 2026"
TICKET_NAME = "General Admission"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        return
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # Make sure website_event is installed so is_published / the
    # Publish switch are available on event.event.
    _ensure_module(env, "website_event")

    prior_events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if prior_events:
        regs = env["event.registration"].with_context(active_test=False).search([
            ("event_id", "in", prior_events.ids),
        ])
        if regs:
            try:
                regs.mapped("registration_answer_ids").sudo().unlink()
            except Exception:
                pass
            try:
                regs.sudo().unlink()
            except Exception:
                pass
        try:
            prior_events.mapped("event_ticket_ids").sudo().unlink()
        except Exception:
            pass
        try:
            prior_events.sudo().unlink()
        except Exception:
            pass

    env.flush_all()
