"""Cleanup for survey.invite_attendees_send_email."""


SURVEY_TITLE = "Bench Onboarding Quiz"
SUBJECT = "Please complete onboarding"
TARGET_EMAILS = ["alice@x.com", "bob@y.com", "carol@z.com"]


def cleanup(env):
    if "survey.survey" not in env.registry:
        return
    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if survey:
        survey.user_input_ids.unlink()
        survey.question_and_page_ids.unlink()
        survey.unlink()
    env["mail.mail"].with_context(active_test=False).search([
        ("subject", "=", SUBJECT),
    ]).unlink()
    for email in TARGET_EMAILS:
        env["res.partner"].with_context(active_test=False).search([
            ("email", "=ilike", email),
        ]).unlink()
    env["ir.mail_server"].with_context(active_test=False).search(
        [("name", "=", "benchmark_fake_smtp")]
    ).unlink()
