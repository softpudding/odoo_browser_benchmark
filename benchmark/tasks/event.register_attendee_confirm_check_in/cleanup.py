"""Cleanup for event.register_attendee_confirm_check_in."""

EVENT_NAME = "Product Update Q2 — Partners Meetup"
ATTENDEE_NAME = "Sofia Reyes"


def cleanup(env):
    env["event.registration"].search([("name", "=", ATTENDEE_NAME)]).unlink()
    env["event.event"].search([("name", "=", EVENT_NAME)]).unlink()
