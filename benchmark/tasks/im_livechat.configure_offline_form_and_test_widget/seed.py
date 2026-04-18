"""Seed for im_livechat.configure_offline_form_and_test_widget."""


CHANNEL_NAME = "After Hours Help"


def setup(env):
    env["im_livechat.channel"].search([("name", "=", CHANNEL_NAME)]).unlink()
