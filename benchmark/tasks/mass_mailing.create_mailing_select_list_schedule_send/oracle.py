"""Oracle for mass_mailing.create_mailing_select_list_schedule_send.

The mailing.mailing form's WYSIWYG iframe editor and the schedule-date
wizard's datetime widget are both too brittle to drive deterministically
with Playwright (see ODOO19_PATTERNS.md §DateTime button/input dual
rendering and the mass_mailing cookbook notes on the WYSIWYG editor).
We navigate to /odoo/email-marketing to prove the route works for admin,
then commit the canonical end state via JSON-RPC:

1. mailing.mailing.create with subject, body, email_from, mailing_model_id
   (mailing.list), contact_list_ids=[Bench Newsletter Subs].
2. mailing.mailing.schedule.date.create + action_schedule_date to fire the
   same code path the 'Schedule' UI button invokes. This flips state to
   'in_queue' and sets schedule_type='scheduled' + schedule_date (UTC).

The browser-use agent is required to perform the same workflow through
the UI; check.py validates the resulting DB state.
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    login,
    navigate,
    run_oracle,
)


SUBJECT = "Spring Promo"
LIST_NAME = "Bench Newsletter Subs"


def oracle(page):
    login(page)
    navigate(page, "/odoo/email-marketing")
    _wait_no_loading(page)

    response = page.evaluate(
        """async ({subject, listName}) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };

            // --- Resolve mailing.list ir.model id ---
            const modelRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'mailing.list']], ['id']],
                kwargs: { limit: 1 },
            });
            const listModelId = modelRes.result?.[0]?.id;
            if (!listModelId) return 'ir.model for mailing.list not found';

            // --- Resolve the seeded Bench Newsletter Subs list ---
            const listRes = await callKw({
                model: 'mailing.list',
                method: 'search_read',
                args: [[['name', '=', listName]], ['id']],
                kwargs: { limit: 1 },
            });
            const listId = listRes.result?.[0]?.id;
            if (!listId) return 'mailing list not found: ' + listName;

            // --- Get admin email_from (DB constraint requires non-null) ---
            const userRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['email', 'partner_id']],
                kwargs: { limit: 1 },
            });
            const userEmail = userRes.result?.[0]?.email
                || (userRes.result?.[0]?.partner_id && userRes.result[0].partner_id[1])
                || 'admin@example.com';

            // --- Cleanup any prior oracle-run mailing ---
            const priorRes = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', subject]], ['id']],
                kwargs: {},
            });
            const priorIds = (priorRes.result || []).map(r => r.id);
            if (priorIds.length) {
                await callKw({
                    model: 'mailing.mailing',
                    method: 'unlink',
                    args: [priorIds],
                    kwargs: {},
                });
            }

            // --- Create the mailing (Email / Mailing List / seeded list / body) ---
            const createRes = await callKw({
                model: 'mailing.mailing',
                method: 'create',
                args: [[{
                    subject: subject,
                    email_from: userEmail,
                    mailing_type: 'mail',
                    mailing_model_id: listModelId,
                    contact_list_ids: [[6, 0, [listId]]],
                    body_html: '<div><p>Save 20%</p></div>',
                    body_arch: '<div><p>Save 20%</p></div>',
                }]],
                kwargs: {},
            });
            let mailingId = createRes.result;
            if (!mailingId) {
                return 'DEBUG create error: ' + JSON.stringify(createRes.error);
            }
            if (Array.isArray(mailingId)) mailingId = mailingId[0];

            // --- Fire the Schedule wizard (same path the 'Schedule' button uses) ---
            // Wizard datetime is expressed in user local tz. The benchmark admin
            // is typically tz='UTC' so '2026-05-20 10:00:00' local == UTC.
            const wizardRes = await callKw({
                model: 'mailing.mailing.schedule.date',
                method: 'create',
                args: [[{
                    mass_mailing_id: mailingId,
                    schedule_date: '2026-05-20 10:00:00',
                }]],
                kwargs: {},
            });
            let wizardId = wizardRes.result;
            if (!wizardId) {
                return 'DEBUG wizard create error: ' + JSON.stringify(wizardRes.error);
            }
            if (Array.isArray(wizardId)) wizardId = wizardId[0];

            const confirmRes = await callKw({
                model: 'mailing.mailing.schedule.date',
                method: 'action_schedule_date',
                args: [[wizardId]],
                kwargs: {},
            });
            if (confirmRes.error) {
                return 'DEBUG action_schedule_date error: ' + JSON.stringify(confirmRes.error);
            }

            const after = await callKw({
                model: 'mailing.mailing',
                method: 'read',
                args: [[mailingId], ['subject', 'state', 'schedule_type',
                                      'schedule_date', 'mailing_model_name',
                                      'contact_list_ids']],
                kwargs: {},
            });
            return after.result?.[0] || ('no read result err=' + JSON.stringify(after.error));
        }""",
        {"subject": SUBJECT, "listName": LIST_NAME},
    )
    if isinstance(response, str):
        raise RuntimeError(f"Oracle JSON-RPC failed: {response}")
    if response.get("state") != "in_queue":
        raise RuntimeError(
            f"Mailing state is {response.get('state')!r}, expected 'in_queue'"
        )
    if response.get("schedule_type") != "scheduled":
        raise RuntimeError(
            f"Mailing schedule_type is {response.get('schedule_type')!r}, expected 'scheduled'"
        )
    if response.get("mailing_model_name") != "mailing.list":
        raise RuntimeError(
            f"mailing_model_name is {response.get('mailing_model_name')!r}, expected 'mailing.list'"
        )
    if not response.get("schedule_date"):
        raise RuntimeError("schedule_date is empty after action_schedule_date")


run_oracle(oracle)
