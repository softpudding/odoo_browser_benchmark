"""Seed for mail.star_and_reply_inbox_message.

Creates a partner "Bench Coordinator" and a mail.message authored by that
partner, addressed to admin via a mail.notification of type "inbox" so the
message appears in admin's Discuss Inbox. The task is to star that message
and post a reply with a specific body.
"""

COORD_NAME = "Bench Coordinator"
COORD_EMAIL = "coord@bench.test"
SEEDED_BODY = "Please confirm receipt of the Q2 status update."
SEEDED_SUBJECT = "Q2 status update - confirmation needed"
REPLY_BODY = "Acknowledged - will follow up by Friday."


def setup(env):
    admin = env.ref("base.user_admin")

    # Create/find the Bench Coordinator partner.
    coordinator = env["res.partner"].search(
        [("name", "=", COORD_NAME)], limit=1
    )
    if not coordinator:
        coordinator = env["res.partner"].create({
            "name": COORD_NAME,
            "email": COORD_EMAIL,
        })
    else:
        if coordinator.email != COORD_EMAIL:
            coordinator.write({"email": COORD_EMAIL})

    # Remove any stray seeded or reply messages from previous runs.
    env["mail.message"].search([
        "|",
        ("subject", "=", SEEDED_SUBJECT),
        ("body", "ilike", SEEDED_BODY),
    ]).unlink()
    env["mail.message"].search([
        ("body", "ilike", REPLY_BODY),
    ]).unlink()

    mt_comment = env.ref("mail.mt_comment")

    # Post the message onto admin's own partner record so the reply
    # composer has a valid parent thread to post into.
    msg = env["mail.message"].create({
        "author_id": coordinator.id,
        "body": f"<p>{SEEDED_BODY}</p>",
        "subject": SEEDED_SUBJECT,
        "message_type": "comment",
        "subtype_id": mt_comment.id,
        "model": "res.partner",
        "res_id": admin.partner_id.id,
    })

    # Create the inbox needaction notification pointing at admin so the
    # message shows up in the Discuss Inbox.
    env["mail.notification"].create({
        "mail_message_id": msg.id,
        "res_partner_id": admin.partner_id.id,
        "notification_type": "inbox",
        "notification_status": "sent",
        "is_read": False,
    })

    # Clear any pre-existing starred flag so we observe the change.
    if admin.partner_id in msg.starred_partner_ids:
        msg.write({"starred_partner_ids": [(3, admin.partner_id.id)]})
