"""Cleanup for im_livechat.configure_channel_then_handle_widget_chat."""


def cleanup(env):
    env["im_livechat.channel"].search([("name", "=", "Bench Support")]).unlink()
    env["mail.canned.response"].search([("source", "=", ":hi")]).unlink()
