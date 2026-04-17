"""Seed for mail.star_message_filter_starred.

Creates three mail.message records directly, addressed to admin as
needaction recipient so they appear in admin's Discuss Inbox. The task
is to star the target one (containing the Q2 cutoff marker).
"""

TARGET_MARKER = "Finance close blocker — action required for Q2 cutoff"
DISTRACTOR_MARKERS = [
    "Office WiFi upgrade – FYI",
    "Welcome lunch sign-up",
]


def setup(env):
    admin = env.ref("base.user_admin")

    author = env["res.users"].search([("login", "=", "marc.demo")], limit=1)
    if not author:
        author = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "email": "marc.demo@example.com",
            "group_ids": [(6, 0, [env.ref("base.group_user").id])],
        })

    # Remove prior test messages by body marker.
    for marker in [TARGET_MARKER] + DISTRACTOR_MARKERS:
        env["mail.message"].search([("body", "ilike", marker)]).unlink()

    mt_comment = env.ref("mail.mt_comment")
    for marker in DISTRACTOR_MARKERS + [TARGET_MARKER]:
        msg = env["mail.message"].create({
            "author_id": author.partner_id.id,
            "body": f"<p><strong>{marker}</strong></p>",
            "subject": marker,
            "message_type": "comment",
            "subtype_id": mt_comment.id,
            "model": "res.partner",
            "res_id": admin.partner_id.id,
        })
        # Create the needaction notification that puts this in admin's
        # Inbox.
        env["mail.notification"].create({
            "mail_message_id": msg.id,
            "res_partner_id": admin.partner_id.id,
            "notification_type": "inbox",
            "notification_status": "sent",
            "is_read": False,
        })

    # Clear any prior starred flag on these messages.
    msgs = env["mail.message"].search([
        ("body", "ilike", TARGET_MARKER),
    ])
    for m in msgs:
        if admin.partner_id in m.starred_partner_ids:
            m.write({"starred_partner_ids": [(3, admin.partner_id.id)]})
