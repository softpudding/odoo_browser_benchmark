"""Seed for mail.mark_message_as_todo_and_resolve.

Creates a channel #benchmarks-ops with a specific message from user
Marc Demo; the task is to reply in-thread to that message.
"""

CHANNEL_NAME = "benchmarks-ops"
TARGET_BODY = (
    "Can we move the 3 AM warehouse sync to 5 AM? "
    "It's colliding with EU backups."
)


def setup(env):
    admin = env.ref("base.user_admin")

    # Ensure Marc Demo exists.
    marc = env["res.users"].search([("name", "=", "Marc Demo")], limit=1)
    if not marc:
        marc = env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "email": "marc.demo@example.com",
            "group_ids": [(6, 0, [env.ref("base.group_user").id])],
        })

    # Clean prior runs.
    prior = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    for ch in prior:
        env["mail.message"].search([
            ("model", "=", "discuss.channel"),
            ("res_id", "=", ch.id),
        ]).unlink()
    prior.unlink()

    # Create the public channel and add admin + marc as members.
    channel = env["discuss.channel"].create({
        "name": CHANNEL_NAME,
        "channel_type": "channel",
        "group_public_id": False,
    })
    channel.add_members(
        partner_ids=[admin.partner_id.id, marc.partner_id.id],
    )

    # Post the anchor message from Marc Demo.
    channel.with_user(marc).message_post(
        body=f"<p>{TARGET_BODY}</p>",
        message_type="comment",
        subtype_xmlid="mail.mt_comment",
    )
