"""Clean up artifacts from previous runs."""


CHANNEL_NAME = "Morning Standups Alpha"


def cleanup(env):
    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    channels.unlink()
