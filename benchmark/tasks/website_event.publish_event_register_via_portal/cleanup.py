"""Cleanup for website_event.publish_event_register_via_portal."""

EVENT_NAME = "Bench Public Day"
ATTENDEE_NAME = "Priya Patel"
ATTENDEE_EMAIL = "priya.patel@example.com"


def cleanup(env):
    # Child-first: remove registrations for this event or attendee.
    env["event.registration"].with_context(active_test=False).search([
        "|", "|",
        ("name", "=", ATTENDEE_NAME),
        ("email", "=", ATTENDEE_EMAIL),
        ("event_id.name", "=", EVENT_NAME),
    ]).sudo().unlink()
    # Remove the event itself.
    env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ]).sudo().unlink()
