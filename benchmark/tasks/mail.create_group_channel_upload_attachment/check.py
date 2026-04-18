"""Postcondition checks for mail.create_group_channel_upload_attachment."""


CHANNEL_NAME = "Bench Project Sync"
ATTACHMENT_NAME = "sync-notes.txt"
BOB_NAME = "Channel Member Bob"
BOB_EMAIL = "channel.bob@bench.test"
ADMIN_NAMES = {"Administrator", "OdooBot Administrator"}


def check(env):
    failures = []

    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if len(channels) == 0:
        return [f"Discuss channel {CHANNEL_NAME!r} not found"]
    if len(channels) > 1:
        failures.append(
            f"Expected exactly one channel named {CHANNEL_NAME!r}, "
            f"found {len(channels)}"
        )
    channel = channels[0]

    # Channel type must be a private group.
    if channel.channel_type != "group":
        failures.append(
            f"Channel type is {channel.channel_type!r}, expected 'group' "
            f"(a private group channel, not a public channel or DM)"
        )

    # Membership: admin and Bob must both be in channel_member_ids.
    member_partners = channel.channel_member_ids.mapped("partner_id")
    member_names = set(member_partners.mapped("name"))

    admin = env.ref("base.user_admin")
    if admin.partner_id not in member_partners:
        failures.append(
            f"Admin partner ({admin.partner_id.display_name}) is not a "
            f"member of channel {CHANNEL_NAME!r}; current members: "
            f"{sorted(member_names)!r}"
        )

    bob_user = env["res.users"].search(
        [("email", "=", BOB_EMAIL)], limit=1
    )
    if not bob_user:
        return [
            f"Seeded user with email {BOB_EMAIL!r} is missing — seed failed"
        ]
    if bob_user.partner_id not in member_partners:
        failures.append(
            f"Seeded user {BOB_NAME!r} is not a member of channel "
            f"{CHANNEL_NAME!r}; current members: {sorted(member_names)!r}"
        )

    # Attachment: at least one ir.attachment named 'sync-notes.txt' linked
    # to the channel must exist.
    attachments = env["ir.attachment"].search([
        ("res_model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
    ])
    matching = attachments.filtered(
        lambda a: (a.name or "").lower() == ATTACHMENT_NAME.lower()
    )
    if len(matching) == 0:
        failures.append(
            f"No ir.attachment named {ATTACHMENT_NAME!r} linked to channel "
            f"{CHANNEL_NAME!r} (id={channel.id}); all attachments on this "
            f"channel: {attachments.mapped('name')!r}"
        )
    else:
        att = matching[0]
        # Sanity check: attachment must have content.
        if not att.datas and not att.raw:
            failures.append(
                f"Attachment {ATTACHMENT_NAME!r} on channel "
                f"{CHANNEL_NAME!r} has empty content"
            )

    return failures
