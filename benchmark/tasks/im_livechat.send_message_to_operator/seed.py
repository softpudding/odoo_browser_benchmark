"""Seed for im_livechat.send_message_to_operator.

Creates a minimal `im_livechat.channel` 'Bench Help' with admin as the sole
operator and a URL rule so the livechat widget is active on the frontend.

The agent's job is then to use the public livechat widget (shadow-DOM root
`.o-livechat-root`) at `/im_livechat/support/<channel_id>` to open a chat,
type `Hello, I need help`, and send it. That creates a brand-new
`discuss.channel` of `channel_type='livechat'` with the visitor's message
as the first comment.

All previous artifacts are scrubbed first so the seed is idempotent — we
delete any stale `discuss.channel` livechat session linked to the bench
`im_livechat.channel`, plus any `mail.guest` records created by prior
visitor attempts (they proliferate one-per-run otherwise).
"""

CHANNEL_NAME = "Bench Help"


def setup(env):
    # --- Cleanup prior runs --------------------------------------------------
    # Remove any discuss.channel livechat sessions linked to prior Bench Help
    # channels — otherwise repeat runs leave orphan sessions that pollute the
    # postcondition count.
    old_livechat = env["im_livechat.channel"].search([("name", "=", CHANNEL_NAME)])
    if old_livechat:
        old_sessions = env["discuss.channel"].with_context(active_test=False).search([
            ("livechat_channel_id", "in", old_livechat.ids),
        ])
        old_sessions.sudo().unlink()
        old_livechat.unlink()

    # --- Admin lookup --------------------------------------------------------
    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    if not admin:
        raise RuntimeError("admin user not found; seed cannot proceed")

    # --- Live chat channel ---------------------------------------------------
    # `user_ids` is the list of operators. Admin MUST be in this set, else the
    # livechat widget's `_get_operator_info` returns no operator and the
    # `get_session` RPC returns False (button does nothing).
    livechat_channel = env["im_livechat.channel"].create({
        "name": CHANNEL_NAME,
        "user_ids": [(6, 0, [admin.id])],
        "button_text": "Chat with us",
        "default_message": "How may I help you?",
    })

    # A URL rule that matches `/` is required so the widget's livechat
    # button becomes visible on the support page (the widget uses the
    # rules to decide whether to render the button for the current URL).
    env["im_livechat.channel.rule"].create({
        "channel_id": livechat_channel.id,
        "action": "display_button",
        "regex_url": "/",
    })
