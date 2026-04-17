"""Seed data for event.publish_event_register_attendee."""


EVENT_NAME = "Field Service Summit 2026"


def _ensure_website_event_module(env):
    website_event = env["ir.module.module"].search([("name", "=", "website_event")], limit=1)
    if not website_event:
        return
    if website_event.state != "installed":
        website_event.button_immediate_install()


def setup(env):
    regs = env["event.registration"].search([("name", "=", "Jordan Rivera")])
    regs.unlink()

    _ensure_website_event_module(env)

    event_fields = {}
    if "website_published" in env["event.event"]._fields:
        event_fields["website_published"] = False
    if "is_published" in env["event.event"]._fields:
        event_fields["is_published"] = False

    event = env["event.event"].search([("name", "=", EVENT_NAME)], limit=1)
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-07-14 09:00:00",
        "date_end": "2026-07-14 17:00:00",
    } | event_fields
    if not event:
        event = env["event.event"].create(values)
    else:
        event.write(values)
