"""Clean up artifacts created by seed/run."""

SURVEY_TITLE = "Bench Screening"
JOB_NAME = "Bench Recruit Lead"
APPLICANT_NAME = "Alice Candidate"


def cleanup(env):
    env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
    ]).unlink()

    jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    if jobs:
        jobs.write({"survey_id": False})
        jobs.unlink()

    if "survey.survey" in env.registry:
        surveys = env["survey.survey"].with_context(active_test=False).search([
            ("title", "=", SURVEY_TITLE),
        ])
        if surveys:
            surveys.question_and_page_ids.unlink()
            surveys.unlink()
