"""Seed data for mail.create_channel_invite_members_post_message.

Create two internal users (Bench Alice, Bench Bob) that the agent must invite
to a newly created public Discuss channel. No channel or messages are
pre-created — the agent must do every step of:

  1. Create a public `#team-bench` channel (channel_type='channel').
  2. Invite Bench Alice + Bench Bob via the Invite People side panel.
  3. Post a 'Welcome team!' message in the channel composer.

Distinct from `mail.create_channel_invite_members` (easy, row 229), which uses
private *group* channel type and does not require posting a message. Distinct
from `mail.create_channel_pin_message_invite_member` (row 167), which pins the
message afterwards.

The seed is idempotent: channels named 'team-bench' from prior runs are
dropped, and the two bench users are created only if missing.
"""


CHANNEL_NAME = "team-bench"

INVITEES = [
    {
        "name": "Bench Alice",
        "login": "bench_alice",
        "email": "bench.alice@example.com",
    },
    {
        "name": "Bench Bob",
        "login": "bench_bob",
        "email": "bench.bob@example.com",
    },
]


def setup(env):
    # --- Cleanup prior runs ---------------------------------------------------
    # Remove any stale channel named 'team-bench' from a previous run.
    env["discuss.channel"].with_context(active_test=False).search(
        [("name", "=", CHANNEL_NAME)]
    ).unlink()

    # --- Ensure invitee users exist ------------------------------------------
    admin = env.ref("base.user_admin")
    internal_group = env.ref("base.group_user").id

    # Pre-create OdooBot DM so it's in the before-state snapshot (otherwise
    # first-time Discuss access auto-creates it mid-run and shows as a stray
    # diff row).
    odoobot = env.ref("base.partner_root")
    env["discuss.channel"].with_user(admin)._get_or_create_chat(
        partners_to=[odoobot.id]
    )

    for spec in INVITEES:
        user = env["res.users"].with_context(active_test=False).search(
            [("login", "=", spec["login"])], limit=1
        )
        if not user:
            user = env["res.users"].with_context(active_test=False).search(
                [("name", "=", spec["name"])], limit=1
            )
        if not user:
            env["res.users"].create({
                "name": spec["name"],
                "login": spec["login"],
                "email": spec["email"],
                "group_ids": [(6, 0, [internal_group])],
            })
        else:
            # Ensure the user is active and has base.group_user so it appears
            # in the Discuss Invite People picker.
            if not user.active:
                user.active = True
            if internal_group not in user.group_ids.ids:
                user.write({"group_ids": [(4, internal_group)]})
            # Normalize display name back to the expected value so prior runs
            # that edited this can't drift the invite picker.
            if user.name != spec["name"]:
                user.partner_id.write({"name": spec["name"]})
