"""Cleanup for mail.create_channel_set_description_pin_welcome."""


def cleanup(env):
    env["discuss.channel"].search([("name", "=", "Launch Bridge Red")]).unlink()
