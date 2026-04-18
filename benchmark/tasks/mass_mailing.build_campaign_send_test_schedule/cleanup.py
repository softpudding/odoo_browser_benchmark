"""Cleanup for mass_mailing.build_campaign_send_test_schedule."""


def cleanup(env):
    env["mailing.mailing"].search([("subject", "=", "Dockside April Bulletin")]).unlink()
    env["mailing.contact"].search([("email", "=", "subscriber@dockside.example.com")]).unlink()
    env["mailing.list"].search([("name", "=", "Dockside Subscribers")]).unlink()
