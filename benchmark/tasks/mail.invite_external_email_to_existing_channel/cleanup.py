"""Cleanup for mail.invite_external_email_to_existing_channel."""


CHANNEL_NAME = "project-discussion"
EXTERNAL_EMAIL = "external-guest@bench.test"


def cleanup(env):
    env["discuss.channel"].with_context(active_test=False).search(
        [("name", "=", CHANNEL_NAME)]
    ).unlink()
    env["mail.mail"].with_context(active_test=False).search(
        [("email_to", "=ilike", EXTERNAL_EMAIL)]
    ).unlink()
    env["mail.guest"].with_context(active_test=False).search(
        [("email", "=ilike", EXTERNAL_EMAIL)]
    ).unlink()
    env["res.partner"].with_context(active_test=False).search(
        [("email", "=ilike", EXTERNAL_EMAIL)]
    ).unlink()
    env["ir.mail_server"].with_context(active_test=False).search(
        [("name", "=", "benchmark_fake_smtp")]
    ).unlink()
