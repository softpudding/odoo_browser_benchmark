"""Oracle for calendar.create_event_with_two_organizers_recurring_weekly.

Creates the recurring weekly event via JSON-RPC (oracle bypass is
explicitly allowed by the benchmark spec — the browser-use agent still
has to solve via the UI). Also triggers set_discuss_videocall_location
to populate videocall_location with a /calendar/join_videocall/... URL.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")
    response = page.evaluate(
        """async () => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };

            // Look up Alice Admin (admin partner) and Bob Test partner ids
            const aliceRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Alice Admin']], ['id']],
                kwargs: { limit: 1 },
            });
            const bobRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Bob Test']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!aliceRes.result?.length) return 'missing Alice Admin partner';
            if (!bobRes.result?.length) return 'missing Bob Test partner';

            const aliceId = aliceRes.result[0].id;
            const bobId = bobRes.result[0].id;

            // Generate a discuss-style videocall URL token. The
            // server method `set_discuss_videocall_location` is a dummy
            // intercepted by the frontend; we craft the URL directly.
            const token = (Math.random().toString(16).slice(2) + Math.random().toString(16).slice(2)).slice(0, 32);
            const videocallUrl = `${window.location.origin}/calendar/join_videocall/${token}`;

            // Create the recurring event with videocall URL up front.
            const createRes = await callKw({
                model: 'calendar.event',
                method: 'create',
                args: [[{
                    name: 'Weekly Standup',
                    start: '2026-06-01 09:00:00',
                    stop: '2026-06-01 09:30:00',
                    allday: false,
                    partner_ids: [[6, 0, [aliceId, bobId]]],
                    recurrency: true,
                    rrule_type: 'weekly',
                    interval: 1,
                    mon: true,
                    tue: false,
                    wed: false,
                    thu: false,
                    fri: false,
                    sat: false,
                    sun: false,
                    end_type: 'end_date',
                    until: '2026-12-31',
                    videocall_location: videocallUrl,
                    access_token: token,
                }]],
                kwargs: {},
            });
            if (createRes.error) return 'create failed: ' + JSON.stringify(createRes.error);

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
