"""Seed for survey.publish_share_via_link_get_url.

Creates a single public-access survey 'Customer Pulse Q2' with one question.
The survey is active with access_mode='public' so the Share dialog will
expose the Survey Link (public URL) immediately.
"""


SURVEY_TITLE = "Customer Pulse Q2"


def _ensure_survey_module(env):
    survey_mod = env["ir.module.module"].search([("name", "=", "survey")], limit=1)
    if survey_mod and survey_mod.state != "installed":
        survey_mod.button_immediate_install()


def setup(env):
    _ensure_survey_module(env)

    if "survey.survey" not in env.registry:
        return

    Survey = env["survey.survey"].with_context(active_test=False)
    existing = Survey.search([("title", "=", SURVEY_TITLE)])
    if existing:
        existing.question_and_page_ids.unlink()
        existing.unlink()

    survey = Survey.create({
        "title": SURVEY_TITLE,
        "description": "<p>Quarterly customer pulse — Q2</p>",
        "survey_type": "survey",
        "questions_layout": "one_page",
        "access_mode": "public",
        "scoring_type": "no_scoring",
        "certification": False,
        "active": True,
    })

    env["survey.question"].create({
        "survey_id": survey.id,
        "title": "How satisfied are you this quarter?",
        "sequence": 10,
        "question_type": "simple_choice",
        "suggested_answer_ids": [
            (0, 0, {"value": "Very satisfied", "sequence": 0}),
            (0, 0, {"value": "Satisfied", "sequence": 1}),
            (0, 0, {"value": "Unsatisfied", "sequence": 2}),
        ],
    })

    # Sanity: an access_token must be auto-generated on create.
    if not survey.access_token:
        # Force re-generation via default if missing.
        survey.write({"access_token": survey._get_default_access_token()})
