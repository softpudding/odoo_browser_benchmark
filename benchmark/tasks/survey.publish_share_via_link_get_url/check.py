"""Postcondition checks for survey.publish_share_via_link_get_url.

Verifies the seeded survey is intact and ready for public sharing:
- Survey 'Customer Pulse Q2' still exists and is active.
- access_mode == 'public' (Anyone with the link).
- access_token is non-null (the public URL is /survey/start/<access_token>).
- Survey was not archived, deleted, or repurposed as a certification.
"""


SURVEY_TITLE = "Customer Pulse Q2"


def check(env):
    failures = []

    if "survey.survey" not in env.registry:
        return ["survey module is not installed"]

    survey = env["survey.survey"].with_context(active_test=False).search([
        ("title", "=", SURVEY_TITLE),
    ], limit=1)
    if not survey:
        return [f"Survey '{SURVEY_TITLE}' not found"]

    if not survey.active:
        failures.append(
            f"Survey '{SURVEY_TITLE}' is archived; expected to remain active"
        )

    if survey.access_mode != "public":
        failures.append(
            f"Survey access_mode is '{survey.access_mode}', expected 'public' "
            "so the share dialog exposes the public Survey Link"
        )

    if not survey.access_token:
        failures.append(
            "Survey access_token is empty; the public share URL cannot be built"
        )

    if survey.certification:
        failures.append("Survey was unexpectedly turned into a certification")

    # The single seeded question must still be present (no destructive edits).
    questions = survey.question_ids
    if len(questions) != 1:
        failures.append(
            f"Expected 1 question on the survey, found {len(questions)} "
            "(survey was modified)"
        )
    elif questions[0].title != "How satisfied are you this quarter?":
        failures.append(
            f"Seeded question was renamed to '{questions[0].title}' "
            "(survey was modified)"
        )

    return failures
