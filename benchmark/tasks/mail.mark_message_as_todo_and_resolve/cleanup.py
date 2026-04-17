"""Cleanup for mail.mark_message_as_todo_and_resolve."""

CHANNEL_NAME = "benchmarks-ops"


def cleanup(env):
    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    for ch in channels:
        env["mail.message"].search([
            ("model", "=", "discuss.channel"),
            ("res_id", "=", ch.id),
        ]).unlink()
    channels.unlink()
