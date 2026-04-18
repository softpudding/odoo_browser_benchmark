"""Oracle for event.create_event_tracks_session_schedule.

Creates the two event.track records on the seeded 'Bench Tech Summit'
event via Odoo JSON-RPC inside a logged-in browser session. Each track
has the exact title, start datetime (UTC, admin tz is UTC), and duration
(hours) specified by the prompt.
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
                args: [[['name', '=', 'Bench Tech Summit']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!events.length) {
                throw new Error("Seeded event 'Bench Tech Summit' not found");
            }
            const eventId = events[0].id;

            // Track 1 — Bench Opening Keynote, 2026-05-10 09:00 UTC, 1.0h.
            unwrapId(await callKw({
                model: 'event.track',
                method: 'create',
                args: [[{
                    name: 'Bench Opening Keynote',
                    event_id: eventId,
                    date: '2026-05-10 09:00:00',
                    duration: 1.0,
                }]],
                kwargs: {},
            }));

            // Track 2 — Bench Closing Panel, 2026-05-10 16:00 UTC, 1.5h.
            unwrapId(await callKw({
                model: 'event.track',
                method: 'create',
                args: [[{
                    name: 'Bench Closing Panel',
                    event_id: eventId,
                    date: '2026-05-10 16:00:00',
                    duration: 1.5,
                }]],
                kwargs: {},
            }));

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
