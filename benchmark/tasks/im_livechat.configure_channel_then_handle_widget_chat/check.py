"""Postcondition checks for im_livechat.configure_channel_then_handle_widget_chat.

PASS when the seeded live chat session has received exactly one admin reply
whose body matches the canned-response substitution text. Rejects the common
failure modes:
  * Agent sent the literal shortcut text ('::hello' / ':hello').
  * Agent typed the substitution text manually with typos / different casing.
  * Agent replied to the wrong channel.
  * Agent posted multiple reply messages.
"""

from odoo.tools import html2plaintext


CHANNEL_NAME = "Visitor #BENCH-359"
EXPECTED_REPLY = "Hi, thanks for reaching out!"


def _norm(text):
    """Normalize: strip HTML, collapse whitespace, strip."""
    if not text:
        return ""
    plain = html2plaintext(text) if "<" in text else text
    return " ".join(plain.split()).strip()


def check(env):
    failures = []

    channels = env["discuss.channel"].search([
        ("name", "=", CHANNEL_NAME),
        ("channel_type", "=", "livechat"),
    ])
    if len(channels) != 1:
        return [
            f"Expected exactly 1 livechat channel named {CHANNEL_NAME!r}, "
            f"found {len(channels)}"
        ]
    channel = channels[0]

    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if not admin:
        return ["admin user not found"]

    # All comment messages on the channel, ordered oldest -> newest.
    messages = env["mail.message"].search(
        [
            ("model", "=", "discuss.channel"),
            ("res_id", "=", channel.id),
            ("message_type", "=", "comment"),
        ],
        order="id asc",
    )

    # Visitor waiting message must still be there (agent should not have deleted).
    visitor_msg = messages.filtered(
        lambda m: "hi there" in _norm(m.body).lower()
        and m.author_id != admin.partner_id
    )
    if not visitor_msg:
        failures.append(
            "Visitor's waiting message 'Hi there' is missing from the channel."
        )

    # Admin replies.
    admin_messages = messages.filtered(lambda m: m.author_id == admin.partner_id)
    if len(admin_messages) == 0:
        return failures + [
            "Admin has not posted any reply in the live chat session."
        ]
    if len(admin_messages) > 1:
        bodies = [_norm(m.body) for m in admin_messages]
        failures.append(
            f"Admin posted {len(admin_messages)} messages, expected exactly 1. "
            f"Bodies: {bodies!r}"
        )

    reply = admin_messages[0]
    reply_body = _norm(reply.body)

    if reply_body != EXPECTED_REPLY:
        failures.append(
            f"Admin reply body is {reply_body!r}, "
            f"expected exactly {EXPECTED_REPLY!r}. "
            f"(If the body contains literal '::hello' or ':hello', the agent "
            f"sent the shortcut text instead of triggering the canned-response "
            f"substitution.)"
        )

    # Admin reply must be posted after the visitor's waiting message.
    if visitor_msg and reply.id <= max(visitor_msg.ids):
        failures.append(
            "Admin reply was not posted AFTER the visitor's waiting message."
        )

    # Sanity: canned response seed survived (agent should not edit it).
    canned = env["mail.canned.response"].search([("source", "=", "hello")])
    if len(canned) != 1:
        failures.append(
            f"Expected exactly 1 canned response with shortcut 'hello', "
            f"found {len(canned)}"
        )
    elif canned.substitution != EXPECTED_REPLY:
        failures.append(
            f"Canned response substitution was modified to {canned.substitution!r}"
        )

    # Sanity: live chat channel config untouched.
    bench = env["im_livechat.channel"].search([("name", "=", "Bench Support")])
    if len(bench) != 1:
        failures.append(
            f"Expected exactly 1 im_livechat.channel 'Bench Support', "
            f"found {len(bench)}"
        )

    return failures
