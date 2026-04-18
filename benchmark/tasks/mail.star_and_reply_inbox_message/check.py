"""Postcondition checks for mail.star_and_reply_inbox_message.

Validates that:
1. The seeded message from Bench Coordinator still exists.
2. The seeded message has starred_partner_ids containing the admin partner.
3. A reply mail.message exists whose body contains the required
   acknowledgement sentence. Preferably the reply is a child (parent_id)
   of the seeded message, but this is not strictly required — matching by
   body is sufficient.
"""

import re

COORD_NAME = "Bench Coordinator"
SEEDED_BODY = "Please confirm receipt of the Q2 status update."
SEEDED_SUBJECT = "Q2 status update - confirmation needed"
REPLY_BODY = "Acknowledged - will follow up by Friday."


def _plain(body):
    text = re.sub(r"<[^>]+>", " ", body or "")
    return " ".join(text.split()).strip()


def check(env):
    failures = []

    admin = env.ref("base.user_admin")

    coordinator = env["res.partner"].search(
        [("name", "=", COORD_NAME)], limit=1
    )
    if not coordinator:
        return [f"Seeded partner '{COORD_NAME}' not found — seed failed"]

    seeded = env["mail.message"].search([
        ("subject", "=", SEEDED_SUBJECT),
        ("author_id", "=", coordinator.id),
    ], limit=1)
    if not seeded:
        # Fallback by body.
        seeded = env["mail.message"].search([
            ("body", "ilike", SEEDED_BODY),
            ("author_id", "=", coordinator.id),
        ], limit=1)
    if not seeded:
        return [
            f"Seeded message from '{COORD_NAME}' with body '{SEEDED_BODY}' "
            f"not found — seed failed"
        ]

    if admin.partner_id not in seeded.starred_partner_ids:
        failures.append(
            f"Seeded message '{SEEDED_BODY}' is not starred by admin "
            f"(starred_partner_ids does not include the admin partner)"
        )

    # Look for a reply message. Accept either an exact body match or a
    # body containing the reply sentence.
    candidates = env["mail.message"].search([
        ("id", "!=", seeded.id),
        ("body", "ilike", REPLY_BODY),
    ])
    reply = None
    for m in candidates:
        if REPLY_BODY in _plain(m.body):
            reply = m
            break

    if not reply:
        failures.append(
            f"No reply mail.message found whose body contains "
            f"'{REPLY_BODY}'"
        )
    else:
        # Sanity: the reply should have been posted by admin.
        if reply.author_id and reply.author_id != admin.partner_id:
            failures.append(
                f"Reply message exists but was authored by "
                f"'{reply.author_id.display_name}' instead of Administrator"
            )

    return failures
