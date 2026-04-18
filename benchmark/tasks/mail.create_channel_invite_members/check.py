"""Postcondition checks for mail.create_channel_invite_members."""


CHANNEL_NAME = "Release Rehearsal Team"
REQUIRED_MEMBER_NAMES = {"Administrator", "Nadia Rossi", "Oliver Chen"}


def check(env):
    failures = []

    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if not channels:
        return [f"Discuss channel {CHANNEL_NAME!r} not found"]
    if len(channels) > 1:
        failures.append(
            f"Expected exactly one channel named {CHANNEL_NAME!r}, "
            f"found {len(channels)}"
        )
    channel = channels[0]

    if channel.channel_type != "group":
        failures.append(
            f"Channel type is {channel.channel_type!r}, expected 'group' "
            f"(a private group channel)"
        )

    member_names = set(channel.channel_member_ids.mapped("partner_id.name"))
    missing = REQUIRED_MEMBER_NAMES - member_names
    if missing:
        failures.append(
            f"Channel is missing required members: {sorted(missing)!r} "
            f"(current members: {sorted(member_names)!r})"
        )

    return failures
