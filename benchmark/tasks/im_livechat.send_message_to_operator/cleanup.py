"""Cleanup for im_livechat.send_message_to_operator."""


def cleanup(env):
    # Find the live chat channel and delete it (with linked sessions) so a
    # subsequent run starts from a clean state.
    bench = env["im_livechat.channel"].search([("name", "=", "Bench Help")])
    if bench:
        sessions = env["discuss.channel"].with_context(active_test=False).search([
            ("livechat_channel_id", "in", bench.ids),
        ])
        sessions.sudo().unlink()
        bench.unlink()
