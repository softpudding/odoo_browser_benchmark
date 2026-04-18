"""Oracle for survey.create_survey_one_page_publish_share.

Builds the single-page customer feedback survey via Odoo JSON-RPC (callKw)
inside a logged-in browser session.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/surveys")
    response = page.evaluate(
        """async () => {
            const unwrapId = (value) => Array.isArray(value) ? value[0] : value;
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            // Create the survey itself (single page, public access so share
            // link works, regular feedback — not a certification).
            const surveyId = unwrapId(await callKw({
                model: 'survey.survey',
                method: 'create',
                args: [[{
                    title: 'Bench Customer Feedback',
                    survey_type: 'survey',
                    questions_layout: 'one_page',
                    access_mode: 'public',
                    scoring_type: 'no_scoring',
                    certification: false,
                    active: true,
                }]],
                kwargs: {},
            }));

            // Page / section "Feedback"
            const pageId = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Feedback',
                    sequence: 10,
                    is_page: true,
                    questions_selection: 'all',
                }]],
                kwargs: {},
            }));

            // Q1 — How satisfied are you? (simple_choice)
            const q1Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    page_id: pageId,
                    title: 'How satisfied are you?',
                    sequence: 20,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value] of [
                [0, 'Very satisfied'],
                [1, 'Satisfied'],
                [2, 'Neutral'],
                [3, 'Unsatisfied'],
            ]) {
                await callKw({
                    model: 'survey.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q1Id,
                        sequence: i,
                        value: value,
                    }]],
                    kwargs: {},
                });
            }

            // Q2 — What can we improve? (text_box)
            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    page_id: pageId,
                    title: 'What can we improve?',
                    sequence: 30,
                    question_type: 'text_box',
                }]],
                kwargs: {},
            });

            // Q3 — Would you recommend us? (simple_choice)
            const q3Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    page_id: pageId,
                    title: 'Would you recommend us?',
                    sequence: 40,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value] of [
                [0, 'Yes'],
                [1, 'No'],
                [2, 'Maybe'],
            ]) {
                await callKw({
                    model: 'survey.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q3Id,
                        sequence: i,
                        value: value,
                    }]],
                    kwargs: {},
                });
            }

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
