"""Oracle for survey.create_certification_quiz_attempt_limit_publish."""

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
                    title: 'Forklift Safety Certification',
                    description: '<p>Pass this certification before operating lift equipment.</p>',
                    survey_type: 'custom',
                    questions_layout: 'page_per_section',
                    access_mode: 'token',
                    scoring_type: 'scoring_with_answers',
                    certification: true,
                    scoring_success_min: 80,
                    is_attempts_limited: true,
                    attempts_limit: 2,
                }]],
                kwargs: {},
            }));

            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Load Handling',
                    sequence: 10,
                    is_page: true,
                    questions_selection: 'all',
                }]],
                kwargs: {},
            });

            const q1Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'What is the maximum load for Bay 3 forklift?',
                    sequence: 20,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value, isCorrect] of [[0, '800 kg', false], [1, '1200 kg', true], [2, '1600 kg', false]]) {
                await callKw({
                    model: 'survey.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q1Id,
                        sequence: i,
                        value,
                        answer_score: isCorrect ? 1 : 0,
                        is_correct: isCorrect,
                    }]],
                    kwargs: {},
                });
            }

            const q2Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'When reversing with a blocked view, what must the operator do?',
                    sequence: 30,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value, isCorrect] of [
                [0, 'Use a spotter', true],
                [1, 'Speed up to clear the aisle', false],
                [2, 'Lift the forks higher', false],
            ]) {
                await callKw({
                    model: 'survey.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q2Id,
                        sequence: i,
                        value,
                        answer_score: isCorrect ? 1 : 0,
                        is_correct: isCorrect,
                    }]],
                    kwargs: {},
                });
            }

            await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Emergency Response',
                    sequence: 40,
                    is_page: true,
                    questions_selection: 'all',
                }]],
                kwargs: {},
            });

            const q3Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'Where is the emergency cutoff for Charging Station B?',
                    sequence: 50,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value, isCorrect] of [
                [0, 'North wall', true],
                [1, 'Inside the battery cabinet', false],
                [2, 'By the loading door', false],
            ]) {
                await callKw({
                    model: 'survey.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q3Id,
                        sequence: i,
                        value,
                        answer_score: isCorrect ? 1 : 0,
                        is_correct: isCorrect,
                    }]],
                    kwargs: {},
                });
            }

            const q4Id = unwrapId(await callKw({
                model: 'survey.question',
                method: 'create',
                args: [[{
                    survey_id: surveyId,
                    title: 'After a hydraulic leak, what is the first action?',
                    sequence: 60,
                    question_type: 'simple_choice',
                }]],
                kwargs: {},
            }));
            for (const [i, value, isCorrect] of [
                [0, 'Shut down the forklift and isolate the area', true],
                [1, 'Finish the delivery before reporting it', false],
                [2, 'Wash the leak into the nearest drain', false],
            ]) {
                await callKw({
                    model: 'survey.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q4Id,
                        sequence: i,
                        value,
                        answer_score: isCorrect ? 1 : 0,
                        is_correct: isCorrect,
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
