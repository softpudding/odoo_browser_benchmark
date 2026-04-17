"""Cleanup for im_livechat.create_channel_add_canned_response."""


def cleanup(env):
    env["im_livechat.channel"].search([("name", "=", "Checkout Support")]).unlink()
    env["mail.canned.response"].search([("source", "=", "checkout_help")]).unlink()
