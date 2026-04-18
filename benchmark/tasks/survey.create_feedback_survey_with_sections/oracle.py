"""Oracle for survey.create_feedback_survey_with_sections.

Builds the feedback survey via Odoo JSON-RPC (callKw) inside a logged-in
browser session, mirroring the structure of survey.branching_quiz_publish_share_link.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-survey.action_survey_form")
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

            // Use survey_type='custom' (default) so the time limit field is
            // available; the spec only forbids 'assessment'.
            const surveyId = unwrapId(await callKw({
                model: 'survey.survey',
                method: 'create',
                args: [[{
                    title: 'Q1 Workshop Feedback',
                    description: '<p>Share your thoughts on the March workshop</p>',
                    survey_type: 'custom',
                    questions_layout: 'page_per_section',
                    access_mode: 'public',
                    is_time_limited: true,
                    time_limit: 10,
                    scoring_type: 'no_scoring',
                    certification: false,
                }]],
                kwargs: {},
            }));

            // Section 1 — Content
            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Content',
                    sequence: 10,
                    is_page: true,
                    questions_selection: 'all',
                }]],
                kwargs: {},
            });

            // Q1 — How clear was the material?
            const q1Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'How clear was the material?',
                    sequence: 20,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value] of [[0, 'Very clear'], [1, 'Clear'], [2, 'Unclear']]) {
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

            // Q2 — Rate the pace (Scale 1-5)
            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Rate the pace',
                    sequence: 30,
                    question_type: 'scale',
                }]],
                kwargs: {},
            });

            // Section 2 — Logistics
            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Logistics',
                    sequence: 40,
                    is_page: true,
                    questions_selection: 'all',
                }]],
                kwargs: {},
            });

            // Q3 — Was the venue comfortable?
            const q3Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Was the venue comfortable?',
                    sequence: 50,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value] of [[0, 'Yes'], [1, 'No']]) {
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

            // Q4 — Comments
            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Comments',
                    sequence: 60,
                    question_type: 'text_box',
                }]],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
