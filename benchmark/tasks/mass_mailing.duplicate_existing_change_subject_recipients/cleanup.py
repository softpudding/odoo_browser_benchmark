"""Cleanup for mass_mailing.duplicate_existing_change_subject_recipients."""


SOURCE_SUBJECT = "Q1 Bulletin Template"
DUP_SUBJECT = "Q2 Bulletin Update"


def cleanup(env):
    env["mailing.mailing"].search([
        ("subject", "in", [SOURCE_SUBJECT, DUP_SUBJECT]),
    ]).unlink()
    env["mailing.list"].search([("name", "=", "Bench Q1 Subscribers")]).unlink()
