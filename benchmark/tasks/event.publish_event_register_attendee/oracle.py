"""Oracle for event.publish_event_register_attendee."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
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
            const eventRes = await callKw({
                model: 'event.event',
                method: 'search_read',
                args: [[['name', '=', 'Field Service Summit 2026']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!eventRes.result?.length) {
                return 'event not found';
            }
            const eventId = eventRes.result[0].id;
            await callKw({
                model: 'event.event',
                method: 'write',
                args: [[eventId], { website_published: true }],
                kwargs: {},
            });
            await callKw({
                model: 'event.registration',
                method: 'create',
                args: [[{
                    event_id: eventId,
                    name: 'Jordan Rivera',
                    email: 'jordan.rivera@example.com',
                    phone: '+1 555 0199',
                }]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
