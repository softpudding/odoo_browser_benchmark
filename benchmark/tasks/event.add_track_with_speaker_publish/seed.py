"""Seed for event.add_track_with_speaker_publish.

Installs website_event / website_event_track on demand so the Tracks smart
button + event.track form are available, then seeds a single target event
'Bench Spring Summit' with no tracks. Agent must create the track.
"""


EVENT_NAME = "Bench Spring Summit"
TRACK_NAME = "Keynote: Future of Bench"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        return
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # Make sure website_event_track (and transitively website_event) are
    # installed — they are not in the base snapshot.
    _ensure_module(env, "website_event")
    _ensure_module(env, "website_event_track")

    # Cleanup prior runs child-first.
    prior_tracks = env["event.track"].with_context(active_test=False).search([
        ("name", "=", TRACK_NAME),
    ])
    prior_tracks.sudo().unlink()

    prior_events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    # Purge any stray tracks on the event from earlier failed runs.
    prior_events.mapped("track_ids").sudo().unlink()
    prior_events.sudo().unlink()

    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-05-15 08:00:00",
        "date_end": "2026-05-16 17:00:00",
    }
    # Keep it unpublished so the diff only captures the track's publish flip.
    if "is_published" in env["event.event"]._fields:
        values["is_published"] = False
    if "website_published" in env["event.event"]._fields:
        values["website_published"] = False

    env["event.event"].create(values)
