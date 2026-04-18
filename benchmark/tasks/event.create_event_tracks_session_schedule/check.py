"""Postcondition checks for event.create_event_tracks_session_schedule."""


EVENT_NAME = "Bench Tech Summit"

# (title, expected date string in UTC, expected duration in hours)
EXPECTED_TRACKS = [
    ("Bench Opening Keynote", "2026-05-10 09:00:00", 1.0),
    ("Bench Closing Panel", "2026-05-10 16:00:00", 1.5),
]


def check(env):
    failures = []

    events = env["event.event"].search([("name", "=", EVENT_NAME)])
    if len(events) != 1:
        return [
            f"Expected exactly 1 event named '{EVENT_NAME}', found {len(events)}"
        ]
    event = events[0]

    tracks = env["event.track"].search([("event_id", "=", event.id)])
    by_name = {t.name: t for t in tracks}

    for title, expected_date, expected_duration in EXPECTED_TRACKS:
        track = by_name.get(title)
        if not track:
            failures.append(
                f"Missing track titled '{title}' on event '{EVENT_NAME}' "
                f"(found: {sorted(by_name)})"
            )
            continue
        if str(track.date) != expected_date:
            failures.append(
                f"Track '{title}' date is {track.date!r}, "
                f"expected '{expected_date}'"
            )
        # Duration is a Float (hours). Use a small epsilon to tolerate any
        # Float -> UI round-tripping noise, but the oracle stores exact values.
        if abs((track.duration or 0.0) - expected_duration) > 1e-4:
            failures.append(
                f"Track '{title}' duration is {track.duration!r}, "
                f"expected {expected_duration}"
            )

    # Guardrail: no extra tracks beyond the two required ones.
    expected_titles = {t[0] for t in EXPECTED_TRACKS}
    extras = [t.name for t in tracks if t.name not in expected_titles]
    if extras:
        failures.append(f"Unexpected extra tracks on event: {extras}")

    return failures
