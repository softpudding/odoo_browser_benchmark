"""Oracle for calendar.invite_organize_with_event_agenda_attachment.

Uses call_kw to deterministically:
  - Create the calendar event 'Q2 Planning Session' on 2026-05-20
    14:00-15:30 (stored in UTC, assuming admin tz is UTC).
  - Attach the two seeded partners Alice Bench + Bob Bench via
    partner_ids.
  - Create an ir.attachment named 'agenda.txt' linked to the event
    (res_model='calendar.event', res_id=event.id) with the agenda file
    content.

Browser-use agents on the same task cannot drive the hidden
``<input type=file>`` behind the chatter paperclip and fail the
attachment check.
"""

import base64
import os
from datetime import datetime

import pytz

from benchmark.oracle_helpers import login, navigate, run_oracle


EVENT_NAME = "Q2 Planning Session"
ATTENDEES = ("Alice Bench", "Bob Bench")
AGENDA_FILENAME = "agenda.txt"

AGENDA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "seed_artifacts",
    AGENDA_FILENAME,
)


def _local_to_utc_iso(tz_name: str, year: int, month: int, day: int, hour: int, minute: int) -> str:
    """Convert (local_tz, Y-M-D H:M) to a naive 'YYYY-MM-DD HH:MM:SS' UTC string."""
    try:
        local_tz = pytz.timezone(tz_name or "UTC")
    except Exception:
        local_tz = pytz.UTC
    local_dt = local_tz.localize(datetime(year, month, day, hour, minute, 0))
    utc_dt = local_dt.astimezone(pytz.UTC)
    return utc_dt.strftime("%Y-%m-%d %H:%M:%S")


def oracle(page):
    login(page)
    navigate(page, "/odoo/calendar")

    # Read the admin user's timezone from the page so we store the event
    # at 14:00-15:30 *local*, which is what the prompt asks for.
    admin_tz = page.evaluate(
        """async () => {
            const res = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'res.users',
                        method: 'search_read',
                        args: [[['login', '=', 'admin']], ['tz']],
                        kwargs: { limit: 1 },
                    },
                }),
            });
            const j = await res.json();
            return (j.result && j.result[0] && j.result[0].tz) || 'UTC';
        }"""
    )

    start_utc = _local_to_utc_iso(admin_tz, 2026, 5, 20, 14, 0)
    stop_utc = _local_to_utc_iso(admin_tz, 2026, 5, 20, 15, 30)

    with open(AGENDA_PATH, "rb") as f:
        agenda_b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "event_name": EVENT_NAME,
        "attendees": list(ATTENDEES),
        "agenda_filename": AGENDA_FILENAME,
        "agenda_b64": agenda_b64,
        "start_utc": start_utc,
        "stop_utc": stop_utc,
    }

    response = page.evaluate(
        """async (payload) => {
            const callKw = async (model, method, args, kwargs) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { model, method, args, kwargs: kwargs || {} },
                    }),
                });
                const j = await res.json();
                if (j.error) {
                    throw new Error(JSON.stringify(j.error));
                }
                return j.result;
            };

            // Resolve partner ids for the two required attendees.
            const partners = await callKw(
                'res.partner',
                'search_read',
                [[['name', 'in', payload.attendees]], ['id', 'name']],
                {},
            );
            const byName = {};
            for (const p of partners) {
                byName[p.name] = p.id;
            }
            const partnerIds = [];
            for (const name of payload.attendees) {
                if (!byName[name]) {
                    throw new Error('Missing seeded partner: ' + name);
                }
                partnerIds.push(byName[name]);
            }

            // Create the calendar event.
            const eventVals = {
                name: payload.event_name,
                start: payload.start_utc,
                stop: payload.stop_utc,
                allday: false,
                recurrency: false,
                partner_ids: [[6, 0, partnerIds]],
            };
            const created = await callKw(
                'calendar.event',
                'create',
                [[eventVals]],
                {},
            );
            const eventId = Array.isArray(created) ? created[0] : created;

            // Create the ir.attachment linked to the event.
            await callKw(
                'ir.attachment',
                'create',
                [[{
                    name: payload.agenda_filename,
                    res_model: 'calendar.event',
                    res_id: eventId,
                    type: 'binary',
                    mimetype: 'text/plain',
                    datas: payload.agenda_b64,
                }]],
                {},
            );

            return 'ok';
        }""",
        payload,
    )

    if response != "ok":
        raise RuntimeError(f"Unexpected oracle response: {response!r}")


run_oracle(oracle)
