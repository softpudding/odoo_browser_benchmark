"""Seed for im_livechat.assign_team_set_offline_form_message.

Creates a fresh "Website Support" live chat channel with the admin user as the
sole operator. The channel's Options-tab text fields (button_text /
default_message) are pinned to the Odoo defaults so the task's edits produce a
clean, deterministic state diff. Any pre-existing channel with the same name
(and its rules) is deleted so the seed is idempotent across re-runs.
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
        # Pin the Options-tab text fields to known defaults so the diff is clean.
        "button_text": "Need help? Chat with us.",
        "default_message": "How may I help you?",
    })
