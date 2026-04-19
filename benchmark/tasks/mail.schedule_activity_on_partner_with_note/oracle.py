"""Oracle for mail.schedule_activity_on_partner_with_note.

Mirrors what the chatter `Schedule Activity` button + wizard do under the
hood when the user picks the default 'To-Do' activity type, fills a
summary, sets a due date, types a note into the HTML editor, and clicks
Schedule. The wizard's `_action_schedule_activities` method delegates to
`self._get_applied_on_records().activity_schedule(...)`, which on
`res.partner` ultimately creates a `mail.activity` row with the supplied
values. We reproduce that exact end state via a single JSON-RPC call.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


PARTNER_NAME = "Bench Activity Partner"
EXPECTED_SUMMARY = "Follow up call"
EXPECTED_DATE = "2026-05-15"
EXPECTED_NOTE_HTML = "<p>Discuss Q2 plan</p>"


def oracle(page):
    login(page)
    # Landing on a live view first so the session cookie + CSRF token are
    # initialised before we call call_kw.
    navigate(page, "/odoo/contacts")

    payload = {
        "partner_name": PARTNER_NAME,
        "summary": EXPECTED_SUMMARY,
        "date_deadline": EXPECTED_DATE,
        "note": EXPECTED_NOTE_HTML,
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

            // 1. Resolve the target partner.
            const partners = await callKw(
                'res.partner',
                'search_read',
                [[['name', '=', payload.partner_name]], ['id', 'name']],
                { limit: 1 },
            );
            if (!partners || !partners.length) {
                throw new Error('Seeded partner not found: ' + payload.partner_name);
            }
            const partnerId = partners[0].id;

            // 2. Resolve the default 'To-Do' activity type. On Odoo 19
            // the canonical xmlid is `mail.mail_activity_data_todo`.
            const todoRows = await callKw(
                'mail.activity.type',
                'search_read',
                [[['name', '=', 'To-Do']], ['id', 'name']],
                { limit: 1 },
            );
            if (!todoRows || !todoRows.length) {
                throw new Error('Activity type To-Do not found');
            }
            const todoId = todoRows[0].id;

            // 3. Delegate to res.partner.activity_schedule — exactly what
            // mail.activity.schedule._action_schedule_activities does in
            // the wizard. This creates a single mail.activity row on the
            // partner with our summary / date_deadline / HTML note.
            // Recordset return serialises as a list of ids through
            // call_kw; we just need the call to succeed without raising.
            await callKw(
                'res.partner',
                'activity_schedule',
                [[partnerId]],
                {
                    activity_type_id: todoId,
                    summary: payload.summary,
                    note: payload.note,
                    date_deadline: payload.date_deadline,
                },
            );

            // 4. Verify: re-fetch the mail.activity row we just created
            // to make sure the wizard-equivalent path persisted.
            const acts = await callKw(
                'mail.activity',
                'search_read',
                [[
                    ['res_model', '=', 'res.partner'],
                    ['res_id', '=', partnerId],
                    ['summary', '=', payload.summary],
                ], ['id', 'summary', 'date_deadline']],
                { limit: 1 },
            );
            return acts && acts.length ? 'ok' : 'no-activity-returned';
        }""",
        payload,
    )

    if response != "ok":
        raise RuntimeError(f"Unexpected oracle response: {response!r}")


run_oracle(oracle)
