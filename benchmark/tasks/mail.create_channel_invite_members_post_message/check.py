"""Postcondition checks for mail.create_channel_invite_members_post_message.

PASS when:
  * Exactly one discuss.channel named 'team-bench' exists.
  * Its channel_type is 'channel' (public), NOT 'group' or 'chat'.
  * Its channel_member_ids include Administrator + Bench Alice + Bench Bob.
  * At least one user mail.message on the channel has body containing
    'Welcome team' (case-insensitive).
"""

from odoo.tools import html2plaintext


CHANNEL_NAME = "team-bench"
REQUIRED_MEMBER_NAMES = {"Administrator", "Mitchell Admin", "Bench Alice", "Bench Bob"}
CORE_MEMBERS = {"Bench Alice", "Bench Bob"}


def _norm(text):
    if not text:
        return ""
    plain = html2plaintext(text) if "<" in text else text
    return " ".join(plain.split()).strip().lower()


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

    if channel.channel_type != "channel":
        failures.append(
            f"Channel type is {channel.channel_type!r}, expected 'channel' "
            f"(a public channel, not 'group' / 'chat' / 'livechat')"
        )

    member_names = set(channel.channel_member_ids.mapped("partner_id.name"))

    # Admin may appear as either 'Administrator' or 'Mitchell Admin' depending
    # on the snapshot. Accept either.
    has_admin = any(n in member_names for n in ("Administrator", "Mitchell Admin"))
    if not has_admin:
        failures.append(
            f"Channel is missing the admin creator as a member "
            f"(current members: {sorted(member_names)!r})"
        )
    missing_bench = CORE_MEMBERS - member_names
    if missing_bench:
        failures.append(
            f"Channel is missing required members: {sorted(missing_bench)!r} "
            f"(current members: {sorted(member_names)!r})"
        )

    # Require at least 3 members total (admin + 2 invitees). Extra members
    # beyond that would mean the agent invited too many people.
    if len(channel.channel_member_ids) < 3:
        failures.append(
            f"Expected >= 3 channel members, found "
            f"{len(channel.channel_member_ids)}"
        )

    # Check a user-posted message contains 'Welcome team'.
    welcome_msgs = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
        ("message_type", "in", ("comment",)),
    ])
    matched = [
        m for m in welcome_msgs
        if "welcome team" in _norm(m.body)
    ]
    if not matched:
        bodies = [(_norm(m.body) or "")[:80] for m in welcome_msgs]
        failures.append(
            f"No user comment on channel {CHANNEL_NAME!r} contains "
            f"'Welcome team'. Observed comment bodies: {bodies!r}"
        )

    return failures
