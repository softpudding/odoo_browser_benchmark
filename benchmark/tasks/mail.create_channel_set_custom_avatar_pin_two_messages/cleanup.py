"""Cleanup for mail.create_channel_set_custom_avatar_pin_two_messages."""


CHANNEL_NAME = "engineering-hub"


def cleanup(env):
    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if channels:
        msgs = env["mail.message"].search([
            ("model", "=", "discuss.channel"),
            ("res_id", "in", channels.ids),
        ])
        if msgs:
            msgs.unlink()
        channels.unlink()
