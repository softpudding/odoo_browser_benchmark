"""Cleanup for event.add_track_with_speaker_publish."""


EVENT_NAME = "Bench Spring Summit"
TRACK_NAME = "Keynote: Future of Bench"


def cleanup(env):
    tracks = env["event.track"].with_context(active_test=False).search([
        ("name", "=", TRACK_NAME),
    ])
    tracks.sudo().unlink()

    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    events.mapped("track_ids").sudo().unlink()
    events.sudo().unlink()
