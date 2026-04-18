"""Cleanup for mail.mark_message_done_archive_notification."""

MESSAGE_SNIPPET = "System maintenance scheduled for Saturday"
AUTHOR_EMAIL = "notifier@bench.test"


def cleanup(env):
    # Delete seeded messages (mail.notification rows cascade via
    # mail_message_id ondelete='cascade').
    msgs = env["mail.message"].search([
        ("body", "ilike", MESSAGE_SNIPPET),
    ])
    msgs.unlink()

    # Delete the seeded sender partner if it has no user attached.
    partners = env["res.partner"].search([
        ("email", "=", AUTHOR_EMAIL),
    ])
    for p in partners:
        if not env["res.users"].search([("partner_id", "=", p.id)], limit=1):
            p.unlink()
