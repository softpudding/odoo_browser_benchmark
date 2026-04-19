"""Cleanup for event.create_event_add_ticket_publish."""


EVENT_NAME = "Bench Summer Summit 2026"


def cleanup(env):
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if not events:
        return

    regs = env["event.registration"].with_context(active_test=False).search([
        ("event_id", "in", events.ids),
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
        events.mapped("event_ticket_ids").sudo().unlink()
    except Exception:
        pass
    try:
        events.sudo().unlink()
    except Exception:
        pass
