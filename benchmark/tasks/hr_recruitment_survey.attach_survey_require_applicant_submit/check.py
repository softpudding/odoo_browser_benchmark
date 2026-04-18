"""Postcondition checks for hr_recruitment_survey.attach_survey_require_applicant_submit.

Validates:
  1. The 'Bench Recruit Lead' hr.job has its survey_id set to the
     'Bench Screening' survey.
  2. The seeded 'Alice Candidate' applicant still exists on that job
     (untouched).
  3. The applicant's related survey_id (computed from job) points to
     Bench Screening — this is the underlying condition that makes the
     'Send Interview' header button render.
  4. No new survey was created by the agent (exactly one Bench Screening
     survey exists, and it is still type 'recruitment').
"""

SURVEY_TITLE = "Bench Screening"
JOB_NAME = "Bench Recruit Lead"
APPLICANT_NAME = "Alice Candidate"


def check(env):
    failures = []

    # 1. Survey exists and has type 'recruitment'
    surveys = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ])
    if len(surveys) != 1:
        failures.append(
            f"Expected exactly 1 survey titled '{SURVEY_TITLE}', found {len(surveys)}"
        )
        return failures
    survey = surveys
    if survey.survey_type != "recruitment":
        failures.append(
            f"Survey '{SURVEY_TITLE}' has survey_type='{survey.survey_type}', "
            "expected 'recruitment'"
        )

    # 2. Job exists and has survey_id = Bench Screening
    job = env["hr.job"].search([("name", "=", JOB_NAME)], limit=1)
    if not job:
        return [f"Job '{JOB_NAME}' not found"]

    if not job.survey_id:
        failures.append(
            f"Job '{JOB_NAME}' has no Interview Form (survey_id is empty)"
        )
    elif job.survey_id.id != survey.id:
        failures.append(
            f"Job '{JOB_NAME}' Interview Form is "
            f"'{job.survey_id.title}', expected '{SURVEY_TITLE}'"
        )

    # 3. Applicant exists on the job and its related survey_id is the
    #    Bench Screening survey (this makes Send Interview visible).
    applicant = env["hr.applicant"].search([
        ("partner_name", "=", APPLICANT_NAME),
        ("job_id", "=", job.id),
    ], limit=1)
    if not applicant:
        failures.append(
            f"Applicant '{APPLICANT_NAME}' not found on job '{JOB_NAME}'"
        )
    else:
        if applicant.survey_id.id != job.survey_id.id:
            failures.append(
                "Applicant.survey_id (related) does not match job.survey_id"
            )
        # Sanity: applicant was not archived or modified.
        if not applicant.active:
            failures.append(f"Applicant '{APPLICANT_NAME}' was archived")

    return failures
