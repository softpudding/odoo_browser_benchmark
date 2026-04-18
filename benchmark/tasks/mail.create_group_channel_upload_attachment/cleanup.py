"""Cleanup for mail.create_group_channel_upload_attachment."""


CHANNEL_NAME = "Bench Project Sync"
ATTACHMENT_NAME = "sync-notes.txt"
BOB_LOGIN = "channel.bob"
BOB_EMAIL = "channel.bob@bench.test"


def cleanup(env):
    # Delete attachments linked to any matching channel first to avoid
    # orphaned ir.attachment rows after channel deletion.
    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if channels:
        env["ir.attachment"].search([
            ("res_model", "=", "discuss.channel"),
            ("res_id", "in", channels.ids),
        ]).unlink()
        channels.unlink()

    # Catch lingering attachments by name (in case channel was already
    # gone but the attachment row remained).
    env["ir.attachment"].search([
        ("name", "=", ATTACHMENT_NAME),
        ("res_model", "=", "discuss.channel"),
    ]).unlink()

    # Remove the seeded Bob user and partner.
    users = env["res.users"].search([
        "|",
        ("login", "=", BOB_LOGIN),
        ("email", "=", BOB_EMAIL),
    ])
    for u in users:
        partner = u.partner_id
        try:
            u.unlink()
        except Exception:
            u.write({"active": False})
            continue
        if partner and not env["res.users"].search(
            [("partner_id", "=", partner.id)], limit=1
        ):
            try:
                partner.unlink()
            except Exception:
                partner.write({"active": False})

    # Catch any partner-only leftover with the test email.
    partners = env["res.partner"].search([("email", "=", BOB_EMAIL)])
    for p in partners:
        if not env["res.users"].search([("partner_id", "=", p.id)], limit=1):
            try:
                p.unlink()
            except Exception:
                p.write({"active": False})
