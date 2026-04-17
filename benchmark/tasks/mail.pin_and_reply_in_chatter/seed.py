"""Seed a Discuss channel with one pre-existing message for pinning."""


CHANNEL_NAME = "Morning Standups Alpha"
SEEDED_BODY = "Print queue alert from warehouse B"
REPLY_BODY = "Acknowledged - investigating now"


def setup(env):
    existing = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    existing.unlink()

    admin = env.ref("base.user_admin")

    # Pre-create the OdooBot DM so it's in the before-state. Without this,
    # first-time Discuss access auto-creates it and shows up as extra edits.
    odoobot = env.ref("base.partner_root")
    env["discuss.channel"].with_user(admin)._get_or_create_chat(
        partners_to=[odoobot.id]
    )
    channel = env["discuss.channel"].create({
        "name": CHANNEL_NAME,
        "channel_type": "channel",
        "channel_partner_ids": [(4, admin.partner_id.id)],
    })

    channel.message_post(
        body=SEEDED_BODY,
        message_type="comment",
        subtype_xmlid="mail.mt_comment",
        author_id=admin.partner_id.id,
    )

    # Clean up any stray reply message from a previous attempt
    stray = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
        ("body", "ilike", REPLY_BODY),
    ])
    stray.unlink()
