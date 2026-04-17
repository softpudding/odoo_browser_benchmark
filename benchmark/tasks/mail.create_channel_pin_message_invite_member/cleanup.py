"""Cleanup for mail.create_channel_pin_message_invite_member."""


def cleanup(env):
    env["discuss.channel"].search([("name", "=", "Ops Escalations Blue")]).unlink()
