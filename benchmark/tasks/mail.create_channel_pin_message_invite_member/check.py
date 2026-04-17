"""Postcondition checks for mail.create_channel_pin_message_invite_member."""


def check(env):
    failures = []
    channel = env["discuss.channel"].search([("name", "=", "Ops Escalations Blue")], limit=1)
    if not channel:
        return ["Discuss channel Ops Escalations Blue not found"]
    if channel.channel_type != "group":
        failures.append(f"Channel type is {channel.channel_type!r}, expected 'group'")

    member_names = set(channel.channel_member_ids.mapped("partner_id.name"))
    expected_members = {"Administrator", "Marc Demo"}
    if not expected_members.issubset(member_names):
        failures.append(f"Channel members are {sorted(member_names)!r}")

    pinned = channel.pinned_message_ids.filtered(
        lambda m: "Please triage the warehouse printer alerts before 4 PM." in (m.body or "")
    )
    if len(pinned) != 1:
        failures.append(f"Expected exactly one pinned target message, found {len(pinned)}")
    return failures
