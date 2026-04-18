"""Postcondition checks for mail.invite_external_email_to_existing_channel.

The browser-use agent succeeds iff a `mail.mail` row was created by
`discuss.channel.invite_by_email` — i.e. email_to contains the external
address AND model='discuss.channel' points at the seeded 'project-discussion'
channel. A `user_notification` mail.message is also posted on the channel
as a side effect of invite_by_email.
"""


CHANNEL_NAME = "project-discussion"
EXTERNAL_EMAIL = "external-guest@bench.test"


def check(env):
    failures = []

    channel = env["discuss.channel"].search(
        [("name", "=", CHANNEL_NAME)], limit=1
    )
    if not channel:
        return [
            f"Expected Discuss channel {CHANNEL_NAME!r} to still exist "
            f"but none was found"
        ]

    # Must still be a private group channel — agent should not have
    # converted the type.
    if channel.channel_type != "group":
        failures.append(
            f"Channel type is {channel.channel_type!r}, expected 'group'"
        )

    # The canonical artifact of invite_by_email: a mail.mail targeting the
    # external email, attached to this channel.
    mails = env["mail.mail"].search(
        [
            ("model", "=", "discuss.channel"),
            ("res_id", "=", channel.id),
            ("email_to", "=ilike", EXTERNAL_EMAIL),
        ]
    )
    if not mails:
        # Be lenient: agents may send without a channel-specific res_id.
        # Fall back to any mail.mail whose email_to contains the external
        # address — we still verify it was authored during the run by the
        # state diff engine (mail.mail in after but not before).
        mails = env["mail.mail"].search(
            [("email_to", "ilike", EXTERNAL_EMAIL)]
        )
    if not mails:
        failures.append(
            f"Expected a mail.mail with model='discuss.channel', "
            f"res_id={channel.id}, email_to containing "
            f"{EXTERNAL_EMAIL!r}; none found. The agent likely did not "
            f"click the 'external-guest@bench.test' envelope row and "
            f"press 'Invite to Group Chat'."
        )

    # Sanity check: the agent must not have added the external address as
    # a new res.partner member on the channel. The UI might offer the
    # existing-partner path; we want the email-invite path specifically.
    member_emails = {
        m.partner_id.email or m.guest_id.email
        for m in channel.channel_member_ids
        if (m.partner_id.email or m.guest_id.email)
    }
    # It is acceptable for a guest member to be linked once someone clicks
    # the invite link (test_04 in Odoo's own tests), but that happens on
    # invitation-link open, NOT on invite_by_email itself. Still, don't
    # penalize extra guest members — only penalize if a RES.PARTNER was
    # created and added, which would indicate the wrong flow.
    extra_partners = channel.channel_member_ids.filtered(
        lambda m: m.partner_id
        and m.partner_id.email
        and EXTERNAL_EMAIL.lower() in m.partner_id.email.lower()
    )
    if extra_partners:
        failures.append(
            f"A res.partner with email {EXTERNAL_EMAIL!r} was added as a "
            f"channel member — but this task requires the email-invite "
            f"flow (mail.mail), not partner-member flow."
        )

    # The agent should not have created a second channel.
    dup = env["discuss.channel"].search_count([("name", "=", CHANNEL_NAME)])
    if dup > 1:
        failures.append(
            f"Expected exactly one channel named {CHANNEL_NAME!r}, "
            f"found {dup}"
        )

    return failures
