"""Postcondition checks for event.add_track_with_speaker_publish."""


EVENT_NAME = "Bench Spring Summit"
TRACK_NAME = "Keynote: Future of Bench"
SPEAKER_NAME = "Dr. Smith"
SPEAKER_EMAIL = "dr.smith@example.com"


def check(env):
    failures = []

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"]
    event = events[0]

    tracks = env["event.track"].search([
        ("event_id", "=", event.id),
        ("name", "=", TRACK_NAME),
    ])
    if len(tracks) != 1:
        return [f"Expected exactly 1 track named '{TRACK_NAME}' on event '{EVENT_NAME}', found {len(tracks)}"]
    track = tracks[0]

    if (track.partner_name or "").strip() != SPEAKER_NAME:
        failures.append(f"Track speaker name is {track.partner_name!r}, expected {SPEAKER_NAME!r}")
    if (track.partner_email or "").strip().lower() != SPEAKER_EMAIL:
        failures.append(f"Track speaker email is {track.partner_email!r}, expected {SPEAKER_EMAIL!r}")

    # Admin tz in the benchmark DB is UTC+8, so "05/15/2026 10:00:00" entered
    # in the UI stores as 2026-05-15 02:00:00 in UTC.
    if str(track.date) != "2026-05-15 02:00:00":
        failures.append(f"Track date is {track.date!r}, expected '2026-05-15 02:00:00'")

    if not track.is_published:
        failures.append("Track is not published (is_published should be True)")

    # Guardrail: no extra tracks on the event.
    other_tracks = env["event.track"].with_context(active_test=False).search([
        ("event_id", "=", event.id),
        ("id", "!=", track.id),
    ])
    if other_tracks:
        failures.append(f"Unexpected extra tracks on event: {other_tracks.mapped('name')}")

    return failures
