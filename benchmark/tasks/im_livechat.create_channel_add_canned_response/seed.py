"""Cleanup-only seed for a live chat channel and canned response task."""


def setup(env):
    env["im_livechat.channel"].search([("name", "=", "Checkout Support")]).unlink()
    env["mail.canned.response"].search([("source", "=", "checkout_help")]).unlink()
