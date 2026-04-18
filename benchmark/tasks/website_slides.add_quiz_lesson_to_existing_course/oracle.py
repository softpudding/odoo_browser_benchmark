"""Oracle for website_slides.add_quiz_lesson_to_existing_course."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/e-learning")
    response = page.evaluate(
        """async () => {
            const unwrap = (value) => Array.isArray(value) ? value[0] : value;
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

            const channels = await callKw({
                model: 'slide.channel',
                method: 'search_read',
                args: [[['name', '=', 'Bench Onboarding Course']], ['id']],
                kwargs: {},
            });
            if (!channels.length) {
                throw new Error('Course "Bench Onboarding Course" not found');
            }
            const channelId = channels[0].id;

            const quizSlideId = unwrap(await callKw({
                model: 'slide.slide',
                method: 'create',
                args: [[{
                    name: 'Chapter 1 Quiz',
                    channel_id: channelId,
                    slide_category: 'quiz',
                    completion_time: 5.0 / 60.0,
                    is_published: true,
                }]],
                kwargs: {},
            }));

            const questions = [
                {
                    title: 'What is the primary color of the Bench logo?',
                    answers: [
                        { text: 'Blue', correct: true },
                        { text: 'Red', correct: false },
                        { text: 'Green', correct: false },
                    ],
                },
                {
                    title: 'How often do we stand up?',
                    answers: [
                        { text: 'Daily', correct: true },
                        { text: 'Weekly', correct: false },
                        { text: 'Never', correct: false },
                    ],
                },
                {
                    title: 'Which team owns shared infra?',
                    answers: [
                        { text: 'Platform', correct: true },
                        { text: 'Product', correct: false },
                        { text: 'Growth', correct: false },
                    ],
                },
            ];

            for (let i = 0; i < questions.length; i++) {
                const q = questions[i];
                const questionId = unwrap(await callKw({
                    model: 'slide.question',
                    method: 'create',
                    args: [[{
                        slide_id: quizSlideId,
                        question: q.title,
                        sequence: (i + 1) * 10,
                    }]],
                    kwargs: {},
                }));
                for (let j = 0; j < q.answers.length; j++) {
                    const a = q.answers[j];
                    await callKw({
                        model: 'slide.answer',
                        method: 'create',
                        args: [[{
                            question_id: questionId,
                            text_value: a.text,
                            is_correct: a.correct,
                            sequence: (j + 1) * 10,
                        }]],
                        kwargs: {},
                    });
                }
            }

            // Ensure published flag is set (create() may not toggle website_published).
            await callKw({
                model: 'slide.slide',
                method: 'write',
                args: [[quizSlideId], { is_published: true }],
                kwargs: {},
            });

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
