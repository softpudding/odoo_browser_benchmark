"""Oracle for event.add_event_questions_to_registration.

Creates the two registration questions on the event via Odoo JSON-RPC
inside a logged-in browser session and links them to the event via the
event_ids many2many field.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
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

            // Find the seeded event by name.
            const events = await callKw({
                model: 'event.event',
                method: 'search_read',
                args: [[['name', '=', 'Bench Tech Conference 2026']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!events.length) {
                throw new Error("Seeded event 'Bench Tech Conference 2026' not found");
            }
            const eventId = events[0].id;

            // Q1 — text input question
            const q1Id = unwrapId(await callKw({
                model: 'event.question',
                method: 'create',
                args: [[{
                    title: 'What is your job title?',
                    question_type: 'text_box',
                    event_ids: [[6, 0, [eventId]]],
                }]],
                kwargs: {},
            }));

            // Q2 — selection question with three answers
            const q2Id = unwrapId(await callKw({
                model: 'event.question',
                method: 'create',
                args: [[{
                    title: 'How many years of experience?',
                    question_type: 'simple_choice',
                    event_ids: [[6, 0, [eventId]]],
                }]],
                kwargs: {},
            }));

            for (const [i, value] of [
                [0, '0-2'],
                [1, '3-5'],
                [2, '5+'],
            ]) {
                await callKw({
                    model: 'event.question.answer',
                    method: 'create',
                    args: [[{
                        question_id: q2Id,
                        sequence: i,
                        name: value,
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
