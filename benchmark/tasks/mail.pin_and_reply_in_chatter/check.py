"""Postcondition checks for mail.pin_and_reply_in_chatter.

Validates that:
1. The seeded channel still exists.
2. The seeded message "Print queue alert from warehouse B" has pinned_at set.
3. A new message with body "Acknowledged - investigating now" exists in the
   same channel and is NOT an internal note.
4. No other messages in the channel were pinned.
"""

import re

CHANNEL_NAME = "Morning Standups Alpha"
SEEDED_BODY = "Print queue alert from warehouse B"
REPLY_BODY = "Acknowledged - investigating now"


def _plain(body):
    text = re.sub(r"<[^>]+>", " ", body or "")
    return " ".join(text.split()).strip()


def check(env):
    failures = []

    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if not channels:
        return [f"Channel '{CHANNEL_NAME}' not found"]
    channel = channels[0]

    messages = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
        ("message_type", "=", "comment"),
    ])

    seeded = None
    reply = None
    other_pinned = []
    for msg in messages:
        text = _plain(msg.body)
        if SEEDED_BODY in text:
            seeded = msg
        elif REPLY_BODY in text:
            reply = msg
        elif getattr(msg, "pinned_at", False):
            other_pinned.append(text[:60])

    if not seeded:
        return [f"Seeded message '{SEEDED_BODY}' not found in channel"]

    if not getattr(seeded, "pinned_at", False):
        failures.append(
            f"Seeded message '{SEEDED_BODY}' is not pinned (pinned_at is not set)"
        )

    if not reply:
        failures.append(
            f"No follow-up message found with body '{REPLY_BODY}' in channel"
        )
    else:
        note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
        if note_subtype and reply.subtype_id == note_subtype:
            failures.append(
                "Follow-up was posted as an internal 'Log note' instead of a "
                "regular message"
            )

    if other_pinned:
        failures.append(
            f"Unexpected pinned messages in channel: {other_pinned}"
        )

    return failures
