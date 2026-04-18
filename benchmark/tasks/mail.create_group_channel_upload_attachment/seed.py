"""Seed for mail.create_group_channel_upload_attachment.

Idempotent: cleans up any prior 'Bench Project Sync' channel and any prior
'Channel Member Bob' user/partner from earlier runs, then ensures a
seeded internal user 'Channel Member Bob' (login 'channel.bob',
email 'channel.bob@bench.test') exists so the agent can invite Bob into
the new group channel.

The channel itself is NOT seeded — the agent must create it.
"""


CHANNEL_NAME = "Bench Project Sync"
ATTACHMENT_NAME = "sync-notes.txt"

BOB_NAME = "Channel Member Bob"
BOB_LOGIN = "channel.bob"
BOB_EMAIL = "channel.bob@bench.test"
BOB_PASSWORD = "bench_pass"


def setup(env):
    # Cleanup prior runs first so the seed is idempotent.
    prior_channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if prior_channels:
        # Remove attachments linked to those channels first to avoid
        # orphaned ir.attachment rows triggering ondelete restrictions.
        env["ir.attachment"].search([
            ("res_model", "=", "discuss.channel"),
            ("res_id", "in", prior_channels.ids),
        ]).unlink()
        prior_channels.unlink()

    # Cleanup any stray attachments by name from previous runs in case the
    # channel was already deleted but the attachment lingered.
    env["ir.attachment"].search([
        ("name", "=", ATTACHMENT_NAME),
        ("res_model", "=", "discuss.channel"),
    ]).unlink()

    # Cleanup prior Bob user (if any) before recreating to ensure the
    # email/login are exactly as expected.
    prior_user = env["res.users"].search([
        "|",
        ("login", "=", BOB_LOGIN),
        ("email", "=", BOB_EMAIL),
    ])
    for u in prior_user:
        partner = u.partner_id
        try:
            u.unlink()
        except Exception:
            # If we can't delete (FK constraint somewhere), at least
            # archive so they don't show up as the active Bob.
            u.write({"active": False})
            continue
        # Try to remove the orphan partner too if no other user uses it.
        if partner and not env["res.users"].search(
            [("partner_id", "=", partner.id)], limit=1
        ):
            try:
                partner.unlink()
            except Exception:
                partner.write({"active": False})

    # Also clean any partner-only leftover with the test email.
    leftover_partners = env["res.partner"].search([
        ("email", "=", BOB_EMAIL),
    ])
    for p in leftover_partners:
        if not env["res.users"].search([("partner_id", "=", p.id)], limit=1):
            try:
                p.unlink()
            except Exception:
                p.write({"active": False})

    internal_group_id = env.ref("base.group_user").id
    env["res.users"].create({
        "name": BOB_NAME,
        "login": BOB_LOGIN,
        "password": BOB_PASSWORD,
        "email": BOB_EMAIL,
        "group_ids": [(6, 0, [internal_group_id])],
    })

    # Pre-create the OdooBot DM so it appears in the before-state. Without
    # this, first-time Discuss access auto-creates it during the run and
    # shows up as a stray discuss.channel diff.
    admin = env.ref("base.user_admin")
    odoobot = env.ref("base.partner_root")
    env["discuss.channel"].with_user(admin)._get_or_create_chat(
        partners_to=[odoobot.id]
    )
