"""Oracle for survey.review_submitted_responses_filter.

Navigates to the seeded survey's participations, locates the participation
whose email matches the target, and posts a chatter "Reviewed" message via
the standard mail.thread message_post route.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


SURVEY_TITLE = "Customer Pulse March"
TARGET_EMAIL = "reviewer-target@example.com"
REVIEW_MESSAGE = "Reviewed: feedback addressed"


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-survey.action_survey_form")
    response = page.evaluate(
        """async ({surveyTitle, targetEmail, reviewMessage}) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: payload,
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(
                        json.error.data?.message || json.error.message
                    );
                }
                return json.result;
            };

            const surveyRes = await callKw({
                model: 'survey.survey',
                method: 'search_read',
                args: [[['title', '=', surveyTitle]], ['id']],
                kwargs: { limit: 1 },
            });
            if (!surveyRes.length) {
                throw new Error('survey not found');
            }
            const surveyId = surveyRes[0].id;

            const inputs = await callKw({
                model: 'survey.user_input',
                method: 'search_read',
                args: [
                    [
                        ['survey_id', '=', surveyId],
                        ['state', '=', 'done'],
                        ['email', '=', targetEmail],
                    ],
                    ['id', 'email'],
                ],
                kwargs: { limit: 1 },
            });
            if (!inputs.length) {
                throw new Error('target participation not found');
            }
            const targetId = inputs[0].id;

            const noteSubtypeRes = await callKw({
                model: 'ir.model.data',
                method: 'check_object_reference',
                args: ['mail', 'mt_comment'],
                kwargs: {},
            });
            const subtypeId = noteSubtypeRes[1];

            await callKw({
                model: 'survey.user_input',
                method: 'message_post',
                args: [[targetId]],
                kwargs: {
                    body: '<p>' + reviewMessage + '</p>',
                    message_type: 'comment',
                    subtype_id: subtypeId,
                },
            });
            return 'ok';
        }""",
        {
            "surveyTitle": SURVEY_TITLE,
            "targetEmail": TARGET_EMAIL,
            "reviewMessage": REVIEW_MESSAGE,
        },
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
