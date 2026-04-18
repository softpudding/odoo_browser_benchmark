"""Seed for im_livechat.configure_url_rule_auto_message.

Creates a fresh "Website Support" live chat channel with the admin user as the
sole operator. Any pre-existing channel with the same name (and its rules) is
deleted so the seed is idempotent across re-runs.
"""


def setup(env):
    # Cleanup prior runs: remove the channel (cascades to rules).
    env["im_livechat.channel"].search([("name", "=", "Website Support")]).unlink()

    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        admin = env["res.users"].search([("login", "=", "admin")], limit=1)

    env["im_livechat.channel"].create({
        "name": "Website Support",
        "user_ids": [(6, 0, [admin.id])] if admin else [(5, 0, 0)],
    })
