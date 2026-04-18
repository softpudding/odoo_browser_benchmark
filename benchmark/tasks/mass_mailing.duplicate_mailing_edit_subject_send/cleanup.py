"""Cleanup for mass_mailing.duplicate_mailing_edit_subject_send."""


SOURCE_SUBJECT = "Bench Newsletter V1"
DUP_SUBJECT = "Bench Newsletter V2 Spring Special"
LIST_NAME = "Bench Subscribers"

CONTACT_EMAILS = [
    "sub1@bench.test",
    "sub2@bench.test",
    "sub3@bench.test",
]


def cleanup(env):
    # Remove any mailings with our two subjects (include variants like "(copy)")
    env["mailing.mailing"].search([
        "|",
        ("subject", "in", [SOURCE_SUBJECT, DUP_SUBJECT]),
        ("subject", "ilike", "Bench Newsletter V"),
    ]).unlink()
    env["mailing.contact"].search([
        ("email", "in", CONTACT_EMAILS),
    ]).unlink()
    env["mailing.list"].search([("name", "=", LIST_NAME)]).unlink()
