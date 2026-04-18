"""Cleanup for event.create_event_tracks_session_schedule."""


EVENT_NAME = "Bench Tech Summit"

TRACK_TITLES = [
    "Bench Opening Keynote",
    "Bench Closing Panel",
]


def cleanup(env):
    # Remove any tracks with the target titles (whether or not still linked).
    tracks = env["event.track"].with_context(active_test=False).search([
        ("name", "in", TRACK_TITLES),
    ])
    tracks.sudo().unlink()

    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    # Remove any leftover tracks on the event, then registrations, then event.
    events.mapped("track_ids").sudo().unlink()
    regs = events.mapped("registration_ids")
    if regs:
        regs.mapped("registration_answer_ids").sudo().unlink()
        regs.sudo().unlink()
    events.sudo().unlink()
