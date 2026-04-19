"""Cleanup for mass_mailing.create_mailing_select_list_schedule_send."""


SUBJECT = "Spring Promo"
LIST_NAME = "Bench Newsletter Subs"

CONTACT_EMAILS = [
    "spring1@bench.test",
    "spring2@bench.test",
    "spring3@bench.test",
]


def cleanup(env):
    env["mailing.mailing"].search([("subject", "=", SUBJECT)]).unlink()
    env["mailing.contact"].search([
        ("email", "in", CONTACT_EMAILS),
    ]).unlink()
    env["mailing.list"].search([("name", "=", LIST_NAME)]).unlink()
