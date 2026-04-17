"""Oracle for survey.branching_quiz_publish_share_link."""

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

            const surveyId = unwrapId(await callKw({
                model: 'survey.survey',
                method: 'create',
                args: [[{
                    title: 'Dock Safety Branching Quiz',
                    survey_type: 'survey',
                    questions_layout: 'one_page',
                    access_mode: 'public',
                    scoring_type: 'scoring_with_answers',
                    users_can_go_back: true,
                }]],
                kwargs: {},
            }));
            const q1Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Which dock zone requires extra clearance tonight?',
                    sequence: 10,
                    question_type: 'simple_choice',
                    constr_mandatory: true,
                }]],
                kwargs: {},
            }));
            const zoneAId = unwrapId(await callKw({
                model: 'survey.question.answer',
                method: 'create',
                args: [[{
                    question_id: q1Id,
                    value: 'Zone A',
                    answer_score: 0,
                    is_correct: false,
                }]],
                kwargs: {},
            }));
            const zoneBId = unwrapId(await callKw({
                model: 'survey.question.answer',
                method: 'create',
                args: [[{
                    question_id: q1Id,
                    value: 'Zone B',
                    answer_score: 1,
                    is_correct: true,
                }]],
                kwargs: {},
            }));
            if (!zoneAId || !zoneBId) {
                throw new Error('failed to create survey answers');
            }
            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Why is Zone B restricted tonight?',
                    sequence: 20,
                    question_type: 'text_box',
                    triggering_answer_ids: [[6, 0, [zoneBId]]],
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
