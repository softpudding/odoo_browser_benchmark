"""Oracle for mass_mailing.build_campaign_send_test_schedule."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/email-marketing")
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
                args: [[['model', '=', 'mailing.list']], ['id']],
                kwargs: { limit: 1 },
            });
            const listRes = await callKw({
                model: 'mailing.list',
                method: 'search_read',
                args: [[['name', '=', 'Dockside Subscribers']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!modelRes.length || !listRes.length) {
                throw new Error('missing mailing list setup');
            }
            const mailingId = unwrapId(await callKw({
                model: 'mailing.mailing',
                method: 'create',
                args: [[{
                    subject: 'Dockside April Bulletin',
                    preview: 'Late berth changes and crane window updates',
                    mailing_type: 'mail',
                    email_from: 'admin@example.com',
                    mailing_model_id: modelRes[0].id,
                    contact_list_ids: [[6, 0, [listRes[0].id]]],
                    body_arch: '<div><p>Late berth changes and crane window updates</p></div>',
                }]],
                kwargs: {},
            }));
            const wizardId = unwrapId(await callKw({
                model: 'mailing.mailing.test',
                method: 'create',
                args: [[{
                    mass_mailing_id: mailingId,
                    email_to: 'admin@example.com',
                }]],
                kwargs: {},
            }));
            await callKw({
                model: 'mailing.mailing.test',
                method: 'send_mail_test',
                args: [[wizardId]],
                kwargs: {},
            });
            const scheduleWizardId = unwrapId(await callKw({
                model: 'mailing.mailing.schedule.date',
                method: 'create',
                args: [[{
                    mass_mailing_id: mailingId,
                    schedule_date: '2026-04-30 09:00:00',
                }]],
                kwargs: {},
            }));
            await callKw({
                model: 'mailing.mailing.schedule.date',
                method: 'action_schedule_date',
                args: [[scheduleWizardId]],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
