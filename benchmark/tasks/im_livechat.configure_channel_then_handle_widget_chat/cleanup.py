"""Cleanup for im_livechat.configure_channel_then_handle_widget_chat."""


def cleanup(env):
    env["discuss.channel"].with_context(active_test=False).search(
        [("name", "=", "Visitor #BENCH-359")]
    ).sudo().unlink()
    env["im_livechat.channel"].search(
        [("name", "=", "Bench Support")]
    ).unlink()
    env["mail.canned.response"].search([("source", "=", "hello")]).unlink()
    env["res.partner"].with_context(active_test=False).search(
        [("name", "=", "Visitor #BENCH-359")]
    ).unlink()
