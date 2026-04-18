"""Cleanup for im_livechat.add_canned_response_send_in_chat."""


def cleanup(env):
    env["mail.canned.response"].search([("source", "=", ":greet")]).unlink()
