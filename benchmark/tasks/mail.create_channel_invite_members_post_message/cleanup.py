"""Cleanup for mail.create_channel_invite_members_post_message."""


CHANNEL_NAME = "team-bench"


def cleanup(env):
    env["discuss.channel"].with_context(active_test=False).search(
        [("name", "=", CHANNEL_NAME)]
    ).unlink()
