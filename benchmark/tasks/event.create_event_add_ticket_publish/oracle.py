"""Oracle for event.create_event_add_ticket_publish.

Pure JSON-RPC oracle. Creates the event.event with the target
date range and one event.event.ticket via a one2many command, then
flips is_published=True. The browser agent must still perform the
same workflow via the UI.

Admin timezone in the benchmark DB is UTC+8, so the prompt's local
times (09:00 and 17:00) translate to UTC as 01:00 and 09:00. We
write the UTC strings directly via JSON-RPC — check.py converts
the stored UTC value back to local for comparison against the
prompt's target values.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


EVENT_NAME = "Bench Summer Summit 2026"
TICKET_NAME = "General Admission"
TICKET_PRICE = 50.0

# Admin tz is UTC+8; 2026-06-15 09:00 local == 2026-06-15 01:00 UTC.
DATE_BEGIN_UTC = "2026-06-15 01:00:00"
DATE_END_UTC = "2026-06-15 09:00:00"


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")

    result = page.evaluate(
        """async (payload) => {
            const unwrapId = (v) => Array.isArray(v) ? v[0] : v;
            const callKw = async (params) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            // Create the event with one ticket via one2many.
            const eventIds = await callKw({
                model: 'event.event',
                method: 'create',
                args: [[{
                    name: payload.eventName,
                    date_begin: payload.dateBegin,
                    date_end: payload.dateEnd,
                    event_ticket_ids: [[0, 0, {
                        name: payload.ticketName,
                        price: payload.ticketPrice,
                    }]],
                }]],
                kwargs: {},
            });
            const eventId = unwrapId(eventIds);

            // Flip is_published=True (website publish).
            await callKw({
                model: 'event.event',
                method: 'write',
                args: [[eventId], { is_published: true }],
                kwargs: {},
            });

            // Sanity read.
            const eventData = await callKw({
                model: 'event.event',
                method: 'read',
                args: [[eventId], ['name', 'date_begin', 'date_end', 'is_published']],
                kwargs: {},
            });
            const tickets = await callKw({
                model: 'event.event.ticket',
                method: 'search_read',
                args: [[['event_id', '=', eventId]], ['name', 'price']],
                kwargs: {},
            });

            return { event: eventData[0], tickets };
        }""",
        {
            "eventName": EVENT_NAME,
            "dateBegin": DATE_BEGIN_UTC,
            "dateEnd": DATE_END_UTC,
            "ticketName": TICKET_NAME,
            "ticketPrice": TICKET_PRICE,
        },
    )

    ev = result["event"]
    tickets = result["tickets"]
    if ev["name"] != EVENT_NAME:
        raise RuntimeError(f"Oracle: event name is {ev['name']!r}, expected {EVENT_NAME!r}")
    if not ev["is_published"]:
        raise RuntimeError("Oracle: event is_published is False, expected True")
    if len(tickets) != 1:
        raise RuntimeError(f"Oracle: expected 1 ticket, got {len(tickets)}")
    tk = tickets[0]
    if tk["name"] != TICKET_NAME:
        raise RuntimeError(f"Oracle: ticket name is {tk['name']!r}, expected {TICKET_NAME!r}")
    if abs(tk["price"] - TICKET_PRICE) > 0.0001:
        raise RuntimeError(f"Oracle: ticket price is {tk['price']}, expected {TICKET_PRICE}")


run_oracle(oracle)
