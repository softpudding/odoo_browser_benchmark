"""Cleanup for im_livechat.configure_url_rule_auto_message."""


def cleanup(env):
    env["im_livechat.channel"].search([("name", "=", "Website Support")]).unlink()
