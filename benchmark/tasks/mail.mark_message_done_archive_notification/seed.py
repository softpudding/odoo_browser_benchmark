"""Seed for mail.mark_message_done_archive_notification.

Creates a partner "Bench Notifier" (as the message author) and a
mail.message that is delivered to admin's Inbox as a needaction
notification (mail.notification with notification_type='inbox',
is_read=False). The task is to mark that notification as done by
clicking the check icon on the message in the Discuss Inbox.
"""

AUTHOR_NAME = "Bench Notifier"
AUTHOR_EMAIL = "notifier@bench.test"
MESSAGE_BODY = "System maintenance scheduled for Saturday."


def setup(env):
    admin = env.ref("base.user_admin")

    # Cleanup prior runs: remove previously seeded messages and the
    # sender partner so seed is idempotent.
    prior_messages = env["mail.message"].search([
        ("body", "ilike", MESSAGE_BODY),
    ])
    prior_messages.unlink()

    prior_partner = env["res.partner"].search([
        ("email", "=", AUTHOR_EMAIL),
    ])
    # Guard: only delete partners that have no user attached to avoid
    # accidentally removing admin-related contacts.
    for p in prior_partner:
        if not env["res.users"].search([("partner_id", "=", p.id)], limit=1):
            p.unlink()

    author = env["res.partner"].create({
        "name": AUTHOR_NAME,
        "email": AUTHOR_EMAIL,
    })

    mt_comment = env.ref("mail.mt_comment")

    msg = env["mail.message"].create({
        "author_id": author.id,
        "body": f"<p>{MESSAGE_BODY}</p>",
        "subject": "System maintenance",
        "message_type": "comment",
        "subtype_id": mt_comment.id,
        "model": "res.partner",
        "res_id": admin.partner_id.id,
    })

    # Create the inbox notification that places the message in admin's
    # Discuss Inbox (is_read=False -> appears in Inbox).
    env["mail.notification"].create({
        "mail_message_id": msg.id,
        "res_partner_id": admin.partner_id.id,
        "notification_type": "inbox",
        "notification_status": "sent",
        "is_read": False,
    })
