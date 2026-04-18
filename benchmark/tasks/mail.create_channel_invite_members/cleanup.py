"""Cleanup for mail.create_channel_invite_members."""


def cleanup(env):
    env["discuss.channel"].search([("name", "=", "Release Rehearsal Team")]).unlink()
