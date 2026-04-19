"""Postcondition checks for im_livechat.send_message_to_operator.

PASS when the public livechat widget has been used to open a new
`discuss.channel` (channel_type='livechat') linked to the seeded
`Bench Help` im_livechat.channel, and that channel has at least one
message whose plain-text body contains the word 'help'. The message
author must be a public/portal identity (guest, public user, or the
seeded visitor partner) — NOT the admin's own res.partner, which
would indicate the agent posted through Discuss back-office instead
of the widget.
"""

from odoo.tools import html2plaintext


CHANNEL_NAME = "Bench Help"


def _norm(text):
    if not text:
        return ""
    plain = html2plaintext(text) if "<" in text else text
    return " ".join(plain.split()).strip()


def check(env):
    failures = []

    # 1. The seeded im_livechat.channel must still exist and not have been
    #    edited in structurally important ways.
    bench = env["im_livechat.channel"].search([("name", "=", CHANNEL_NAME)])
    if len(bench) != 1:
        return [
            f"Expected exactly 1 im_livechat.channel {CHANNEL_NAME!r}, "
            f"found {len(bench)}"
        ]

    # 2. At least one discuss.channel (livechat) linked to this channel.
    sessions = env["discuss.channel"].with_context(active_test=False).search([
        ("channel_type", "=", "livechat"),
        ("livechat_channel_id", "=", bench.id),
    ])
    if len(sessions) == 0:
        return failures + [
            "No discuss.channel of type 'livechat' exists for "
            f"{CHANNEL_NAME!r}. The widget flow did not create a session."
        ]

    # 3. Find a session that has the 'help' message. (Some setups produce
    #    multiple proto-channels if the widget was opened but not sent;
    #    we accept the first session with a matching message.)
    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if not admin:
        return failures + ["admin user not found"]

    matching_session = None
    matching_message = None
    for session in sessions:
        msgs = env["mail.message"].search(
            [
                ("model", "=", "discuss.channel"),
                ("res_id", "=", session.id),
                ("message_type", "in", ("comment", "whatsapp_message")),
            ],
            order="id asc",
        )
        for m in msgs:
            body_txt = _norm(m.body).lower()
            if "help" in body_txt and m.author_id != admin.partner_id:
                matching_session = session
                matching_message = m
                break
        if matching_session:
            break

    if not matching_session:
        # Report what we did find to aid debugging.
        all_msgs = env["mail.message"].search(
            [
                ("model", "=", "discuss.channel"),
                ("res_id", "in", sessions.ids),
                ("message_type", "in", ("comment", "whatsapp_message")),
            ],
            order="id asc",
        )
        bodies = [
            (
                m.author_id.name or "?",
                _norm(m.body)[:80],
            )
            for m in all_msgs
        ]
        return failures + [
            "No livechat session has a visitor message whose body "
            f"contains 'help'. Observed messages across {len(sessions)} "
            f"livechat session(s): {bodies!r}"
        ]

    # 4. Sanity: the matching message should actually be a visitor
    #    message (public/portal author). We already ensured it is not
    #    authored by admin.partner_id. Accept guest authors (author_id
    #    False + author_guest_id set) OR a non-internal author_id.
    if matching_message.author_id:
        # Author is a partner — must not be an internal user.
        author_user = env["res.users"].search(
            [("partner_id", "=", matching_message.author_id.id)], limit=1
        )
        if author_user and author_user.has_group("base.group_user"):
            failures.append(
                "Visitor message is authored by internal user "
                f"{author_user.login!r} (partner id={matching_message.author_id.id}), "
                "expected a public/portal visitor."
            )

    # 5. Sanity: the matching message body actually contains the expected
    #    send text. We tolerate extra whitespace/punctuation but require
    #    the substring 'Hello' and 'help' both appearing.
    body_txt = _norm(matching_message.body).lower()
    if "hello" not in body_txt:
        failures.append(
            f"Visitor message body {_norm(matching_message.body)!r} does not "
            "contain the word 'Hello' — did the agent send a different text?"
        )

    return failures
