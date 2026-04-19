"""Oracle for event.create_event_add_question_publish.

Browser-agent UI-path solution: create the event + two questions via
JSON-RPC, then call `website_publish_button()` to flip both
`is_published` and `website_published` (the same method the website
preview systray toggle calls). JSON-RPC bypass for oracles is
explicitly sanctioned (see ODOO19_PATTERNS.md 'Oracle patterns'); the
browser-use agent must still solve via the UI.

Event-form Questions tab → m2m selector → New question form + nested
answers is fragile under Playwright (the m2m selector dialog is Owl-
rendered and the nested answer tab opens in a second dialog), so UI
automation is not worth the brittleness here.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


EVENT_NAME = "Bench 2026 Conference"
Q1_TITLE = "Company"
Q2_TITLE = "Experience Level"
Q2_ANSWERS = ["Beginner", "Intermediate", "Expert"]


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)

    response = page.evaluate(
        """async (payload) => {
            const unwrap = (value) => Array.isArray(value) ? value[0] : value;
            const callKw = async (p) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0', method: 'call', params: p,
                    }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(
                        json.error.data?.message || json.error.message || 'rpc error'
                    );
                }
                return json.result;
            };

            const {eventName, q1Title, q2Title, q2Answers} = payload;

            // --- Create Question 1 (Text Input, mandatory, per-attendee) ---
            const q1Id = unwrap(await callKw({
                model: 'event.question',
                method: 'create',
                args: [[{
                    title: q1Title,
                    question_type: 'text_box',
                    is_mandatory_answer: true,
                    once_per_order: false,
                }]],
                kwargs: {},
            }));

            // --- Create Question 2 (Selection, mandatory) with nested answers ---
            const q2Id = unwrap(await callKw({
                model: 'event.question',
                method: 'create',
                args: [[{
                    title: q2Title,
                    question_type: 'simple_choice',
                    is_mandatory_answer: true,
                    once_per_order: false,
                    answer_ids: q2Answers.map((name, i) => [0, 0, {
                        name: name,
                        sequence: (i + 1) * 10,
                    }]),
                }]],
                kwargs: {},
            }));

            // --- Create the event, linking both new questions (plus defaults) ---
            const eventId = unwrap(await callKw({
                model: 'event.event',
                method: 'create',
                args: [[{
                    name: eventName,
                    date_begin: '2026-07-15 09:00:00',
                    date_end: '2026-07-16 17:00:00',
                }]],
                kwargs: {},
            }));

            // Append our new questions to whatever _compute_question_ids put there.
            await callKw({
                model: 'event.event',
                method: 'write',
                args: [[eventId], {
                    question_ids: [[4, q1Id], [4, q2Id]],
                }],
                kwargs: {},
            });

            // --- Publish: flip is_published + website_published ---
            // website_publish_button() is what the Owl systray toggle calls.
            await callKw({
                model: 'event.event',
                method: 'website_publish_button',
                args: [[eventId]],
                kwargs: {},
            });

            // Defensive: ensure is_published is true too (the button writes
            // website_published which has an inverse that sets is_published,
            // but do a belt-and-suspenders write).
            await callKw({
                model: 'event.event',
                method: 'write',
                args: [[eventId], {is_published: true}],
                kwargs: {},
            });

            return 'ok';
        }""",
        {
            "eventName": EVENT_NAME,
            "q1Title": Q1_TITLE,
            "q2Title": Q2_TITLE,
            "q2Answers": Q2_ANSWERS,
        },
    )
    if response != "ok":
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")


run_oracle(oracle)
