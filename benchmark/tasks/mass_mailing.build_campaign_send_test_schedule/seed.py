"""Seed for mass_mailing.build_campaign_send_test_schedule."""


def setup(env):
    env["mailing.mailing"].search([("subject", "=", "Dockside April Bulletin")]).unlink()
    env["mailing.contact"].search([("email", "=", "subscriber@dockside.example.com")]).unlink()
    env["mailing.list"].search([("name", "=", "Dockside Subscribers")]).unlink()

    mailing_list = env["mailing.list"].create({"name": "Dockside Subscribers"})
    contact = env["mailing.contact"].create({
        "name": "Dockside Subscriber",
        "email": "subscriber@dockside.example.com",
    })
    contact.subscription_ids = [(0, 0, {"list_id": mailing_list.id, "opt_out": False})]
