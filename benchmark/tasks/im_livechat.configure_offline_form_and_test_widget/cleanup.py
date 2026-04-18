"""Cleanup for im_livechat.configure_offline_form_and_test_widget."""


def cleanup(env):
    env["im_livechat.channel"].search([("name", "=", "After Hours Help")]).unlink()
