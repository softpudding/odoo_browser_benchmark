"""Seed for mail.send_direct_message_to_user.

Admin sends a DM to Priya Mehta with a specific sentence. Seed ensures
Priya exists as a user and that no prior DM between admin and Priya
contains the target sentence.
"""

EXPECTED_SENTENCE = (
    "The 10:00 product sync is moved to Thursday 14:00 — please update "
    "your calendar."
)


def setup(env):
    admin = env.ref("base.user_admin")

    user = env["res.users"].search([("name", "=", "Priya Mehta")], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": "Priya Mehta",
            "login": "priya.mehta",
            "email": "priya.mehta@example.com",
            "group_ids": [(6, 0, [env.ref("base.group_user").id])],
        })

    # Clean up any prior DM thread between admin and Priya so we start fresh.
    existing = env["discuss.channel"].search([
        ("channel_type", "=", "chat"),
        ("channel_member_ids.partner_id", "=", admin.partner_id.id),
    ])
    for ch in existing:
        partners = ch.channel_partner_ids
        if user.partner_id in partners and admin.partner_id in partners and len(partners) == 2:
            # Delete all messages in this DM.
            env["mail.message"].search([
                ("model", "=", "discuss.channel"),
                ("res_id", "=", ch.id),
            ]).unlink()
            ch.unlink()

    # Pre-create the DM channel so the agent only needs to send a message,
    # not navigate Discuss' hidden sidebar '+' button. This keeps the task
    # focused on "send a message" which is what we validate.
    env["discuss.channel"].with_user(admin)._get_or_create_chat(
        partners_to=[user.partner_id.id],
    )
