"""Oracle for calendar.create_private_meeting_with_video_link."""

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
            const marcRes = await callKw({
                model: 'res.partner',
                method: 'search_read',
                args: [[['name', '=', 'Marc Demo']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!marcRes.result?.length) {
                return 'missing Marc Demo partner';
            }
            const createRes = await callKw({
                model: 'calendar.event',
                method: 'create',
                args: [[{
                    name: 'Private Vendor Sync',
                    start: '2026-05-27 14:00:00',
                    stop: '2026-05-27 15:00:00',
                    location: 'Bridge Room',
                    privacy: 'private',
                    description: '<p>Review blocker owners and confirm the supplier handoff plan.</p>',
                    videocall_location: '/calendar/join_videocall/private-vendor-sync',
                    partner_ids: [[6, 0, [marcRes.result[0].id]]],
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
