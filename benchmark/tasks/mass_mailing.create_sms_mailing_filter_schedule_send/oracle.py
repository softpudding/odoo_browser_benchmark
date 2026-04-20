"""Oracle for mass_mailing.create_sms_mailing_filter_schedule_send."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/sms-marketing")
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

            const modelRes = await callKw({
                model: 'ir.model',
                method: 'search_read',
                args: [[['model', '=', 'res.partner']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!modelRes.length) {
                throw new Error('missing res.partner ir.model');
            }

            const existing = await callKw({
                model: 'mailing.mailing',
                method: 'search_read',
                args: [[['subject', '=', 'Berlin Ops SMS']], ['id']],
                kwargs: {},
            });
            const existingIds = (existing || []).map(r => r.id);
            if (existingIds.length) {
                await callKw({
                    model: 'mailing.mailing',
                    method: 'unlink',
                    args: [existingIds],
                    kwargs: {},
                });
            }

            const mailingId = unwrapId(await callKw({
                model: 'mailing.mailing',
                method: 'create',
                args: [[{
                    subject: 'Berlin Ops SMS',
                    mailing_type: 'sms',
                    mailing_model_id: modelRes[0].id,
                    contact_list_ids: [[5, 0, 0]],
                    mailing_domain: "[('city', '=', 'Berlin')]",
                    body_plaintext: 'Berlin operations update: dock check at 09:00.',
                    body_arch: '<p>Berlin operations update: dock check at 09:00.</p>',
                }]],
                kwargs: {},
            }));

            const wizardId = unwrapId(await callKw({
                model: 'mailing.mailing.schedule.date',
                method: 'create',
                args: [[{
                    mass_mailing_id: mailingId,
                    schedule_date: '2026-06-01 01:00:00',
                }]],
                kwargs: {},
            }));
            await callKw({
                model: 'mailing.mailing.schedule.date',
                method: 'action_schedule_date',
                args: [[wizardId]],
                kwargs: {},
            });

            const finalState = await callKw({
                model: 'mailing.mailing',
                method: 'read',
                args: [[mailingId], ['subject', 'mailing_type', 'schedule_date', 'state']],
                kwargs: {},
            });
            return finalState[0];
        }""",
    )
    if response.get("mailing_type") != "sms":
        raise RuntimeError(f"mailing_type is {response.get('mailing_type')!r}")
    if response.get("schedule_date") != "2026-06-01 01:00:00":
        raise RuntimeError(f"schedule_date is {response.get('schedule_date')!r}")


run_oracle(oracle)
