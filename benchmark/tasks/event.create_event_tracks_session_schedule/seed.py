"""Seed for event.create_event_tracks_session_schedule.

Installs website_event / website_event_track on demand so the Tracks smart
button + event.track form are available, then seeds a single published
target event 'Bench Tech Summit' with no tracks. Agent must create the
two conference tracks described in the prompt.
"""


EVENT_NAME = "Bench Tech Summit"

# Track titles the agent will create — clean these up so reruns are idempotent.
TRACK_TITLES = [
    "Bench Opening Keynote",
    "Bench Closing Panel",
]


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

    # Cleanup prior runs child-first: remove any stray tracks with those
    # titles (from previous partial runs or the oracle).
    prior_tracks = env["event.track"].with_context(active_test=False).search([
        ("name", "in", TRACK_TITLES),
    ])
    prior_tracks.sudo().unlink()

    prior_events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    # Purge any stray tracks on the event from earlier failed runs.
    prior_events.mapped("track_ids").sudo().unlink()
    # Detach registration answers before unlinking registrations.
    regs = prior_events.mapped("registration_ids")
    if regs:
        regs.mapped("registration_answer_ids").sudo().unlink()
        regs.sudo().unlink()
    prior_events.sudo().unlink()

    env.flush_all()

    # Create the event — published with website_track enabled so the Tracks
    # smart button is visible on the form and the agent can create tracks.
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-05-10 08:00:00",
        "date_end": "2026-05-10 20:00:00",
    }
    if "website_track" in env["event.event"]._fields:
        values["website_track"] = True
    if "is_published" in env["event.event"]._fields:
        values["is_published"] = True
    if "website_published" in env["event.event"]._fields:
        values["website_published"] = True

    env["event.event"].create(values)
