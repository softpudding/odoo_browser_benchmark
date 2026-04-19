"""Cleanup seed for im_livechat.configure_channel_then_handle_widget_chat.

Ensures the admin user exists and removes any prior-run records so the
task starts from a clean state.
"""


def setup(env):
    # Remove any prior Bench Support channels from failed runs
    env["im_livechat.channel"].search([("name", "=", "Bench Support")]).unlink()

    # Remove any prior :hi canned responses from failed runs
    env["mail.canned.response"].search([("source", "=", ":hi")]).unlink()

    # Ensure the admin user exists (Mitchell Admin / base.user_admin)
    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if not admin:
        raise RuntimeError("Administrator user (base.user_admin) is missing")
