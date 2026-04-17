"""Cleanup for mail.send_direct_message_to_user."""


def cleanup(env):
    admin = env.ref("base.user_admin")
    user = env["res.users"].search([("name", "=", "Priya Mehta")], limit=1)
    if not user:
        return
    chats = env["discuss.channel"].search([("channel_type", "=", "chat")])
    for ch in chats:
        partners = ch.channel_partner_ids
        if (
            admin.partner_id in partners
            and user.partner_id in partners
            and len(partners) == 2
        ):
            env["mail.message"].search([
                ("model", "=", "discuss.channel"),
                ("res_id", "=", ch.id),
            ]).unlink()
            ch.unlink()
