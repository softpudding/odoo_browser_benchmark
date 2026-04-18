"""Postcondition checks for mail.create_channel_set_custom_avatar_pin_two_messages."""


CHANNEL_NAME = "engineering-hub"
EXPECTED_DESCRIPTION = "Weekly engineering updates"
MESSAGES = [
    "Weekly standup Monday 10am",
    "Please review PR #1042",
    "Reminder: retro on Thursday",
]
PINNED_BODIES = {
    "Weekly standup Monday 10am",
    "Reminder: retro on Thursday",
}
NOT_PINNED_BODY = "Please review PR #1042"


def _body_contains(body, snippet):
    return snippet in (body or "")


def check(env):
    failures = []

    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if len(channels) == 0:
        return [f"Discuss channel {CHANNEL_NAME!r} not found"]
    if len(channels) > 1:
        failures.append(f"Expected exactly 1 channel named {CHANNEL_NAME!r}, found {len(channels)}")
    channel = channels[0]

    if channel.channel_type != "channel":
        failures.append(
            f"Channel type is {channel.channel_type!r}, expected 'channel' (public)"
        )

    if (channel.description or "").strip() != EXPECTED_DESCRIPTION:
        failures.append(
            f"Channel description is {channel.description!r}, expected {EXPECTED_DESCRIPTION!r}"
        )

    if not channel.image_128:
        failures.append("Channel image_128 is empty (custom avatar was not uploaded)")

    # Collect messages on this channel.
    msgs = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
        ("message_type", "in", ("comment", "notification")),
    ])

    # Filter to messages whose body matches one of the three expected bodies.
    matched = {snippet: msgs.filtered(lambda m, s=snippet: _body_contains(m.body, s))
               for snippet in MESSAGES}

    for snippet, found in matched.items():
        if len(found) == 0:
            failures.append(f"Missing message: {snippet!r}")
        elif len(found) > 1:
            failures.append(
                f"Found {len(found)} messages matching {snippet!r}, expected 1"
            )

    # Pin checks: exactly the two expected bodies are pinned, the PR
    # message must NOT be pinned.
    pinned = msgs.filtered(lambda m: m.pinned_at)
    pinned_bodies_seen = set()
    for m in pinned:
        for snippet in MESSAGES:
            if _body_contains(m.body, snippet):
                pinned_bodies_seen.add(snippet)
                break

    if len(pinned) != 2:
        failures.append(
            f"Expected exactly 2 pinned messages in the channel, found {len(pinned)}"
        )

    missing_pins = PINNED_BODIES - pinned_bodies_seen
    if missing_pins:
        failures.append(
            f"Required pinned messages missing: {sorted(missing_pins)!r}"
        )

    if NOT_PINNED_BODY in pinned_bodies_seen:
        failures.append(
            f"Distractor message {NOT_PINNED_BODY!r} must NOT be pinned"
        )

    return failures
