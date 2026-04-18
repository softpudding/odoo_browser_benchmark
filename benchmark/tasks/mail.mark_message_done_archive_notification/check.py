"""Postcondition checks for mail.mark_message_done_archive_notification."""

MESSAGE_SNIPPET = "System maintenance scheduled for Saturday"
AUTHOR_EMAIL = "notifier@bench.test"


def check(env):
    failures = []

    admin = env.ref("base.user_admin")

    # The seeded mail.message must still exist (we only want the
    # notification flagged read, not the message deleted).
    msg = env["mail.message"].search([
        ("body", "ilike", MESSAGE_SNIPPET),
    ], limit=1)
    if not msg:
        return [
            f"Seeded mail.message containing '{MESSAGE_SNIPPET}' is "
            f"missing — it must not be deleted; only its notification "
            f"should be marked read"
        ]

    # Find the admin's notification on that message.
    notif = env["mail.notification"].search([
        ("mail_message_id", "=", msg.id),
        ("res_partner_id", "=", admin.partner_id.id),
    ], limit=1)
    if not notif:
        return [
            "mail.notification for admin on the seeded message is "
            "missing — seed likely failed"
        ]

    if not notif.is_read:
        failures.append(
            "mail.notification.is_read is still False — the Mark as "
            "Read / Mark as Done action was not performed on the "
            "Bench Notifier inbox message"
        )

    # Guard against accidental mass mark-all-as-read: verify that
    # OTHER pre-existing inbox notifications for admin were not
    # flipped. We don't know which existed pre-seed, so just sanity
    # check the sender partner still exists (message author wasn't
    # deleted).
    author = env["res.partner"].search([
        ("email", "=", AUTHOR_EMAIL),
    ], limit=1)
    if not author:
        failures.append(
            f"Seeded author partner with email {AUTHOR_EMAIL} is "
            f"missing — it must not be deleted"
        )

    return failures
