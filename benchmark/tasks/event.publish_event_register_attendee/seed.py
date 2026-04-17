"""Seed data for event.publish_event_register_attendee."""


EVENT_NAME = "Field Service Summit 2026"


def setup(env):
    regs = env["event.registration"].search([("name", "=", "Jordan Rivera")])
    regs.unlink()

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-07-14 09:00:00",
        "date_end": "2026-07-14 17:00:00",
        "website_published": False,
        "is_published": False,
    }
    if not event:
        event = env["event.event"].create(values)
    else:
        event.write(values)
