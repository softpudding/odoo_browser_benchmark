"""Postcondition checks for mail.create_channel_set_description_pin_welcome."""


def check(env):
    failures = []
    channel = env["discuss.channel"].search([("name", "=", "Launch Bridge Red")], limit=1)
    if not channel:
        return ["Discuss channel Launch Bridge Red not found"]
    if channel.channel_type != "group":
        failures.append(f"Channel type is {channel.channel_type!r}, expected 'group'")
    if channel.description != "Private launch coordination room for the red deployment wave.":
        failures.append(f"Channel description is {channel.description!r}")

    member_names = set(channel.channel_member_ids.mapped("partner_id.name"))
    expected_members = {"Administrator", "Marc Demo"}
    if member_names != expected_members:
        failures.append(f"Channel members are {sorted(member_names)!r}")

    pinned = channel.pinned_message_ids.filtered(
        lambda m: "Welcome to Launch Bridge Red. Post deployment blockers here." in (m.body or "")
    )
    if len(pinned) != 1:
        failures.append(f"Expected exactly one pinned target message, found {len(pinned)}")
    return failures
