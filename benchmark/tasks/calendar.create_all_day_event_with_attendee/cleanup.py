"""Cleanup for calendar.create_all_day_event_with_attendee."""


def cleanup(env):
    env["calendar.event"].search([("name", "=", "Operations Offsite")]).unlink()
