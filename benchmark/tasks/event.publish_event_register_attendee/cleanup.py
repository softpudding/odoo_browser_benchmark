"""Cleanup for event.publish_event_register_attendee."""


def cleanup(env):
    regs = env["event.registration"].search([("name", "=", "Jordan Rivera")])
    regs.unlink()
    event = env["event.event"].search([("name", "=", "Field Service Summit 2026")], limit=1)
    if event:
        if "website_published" in env["event.event"]._fields:
            event.website_published = False
        if "is_published" in env["event.event"]._fields:
            event.is_published = False
