"""Oracle for mail.create_channel_pin_message_invite_member."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
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
            const adminUser = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            const marcUser = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['name', '=', 'Marc Demo']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            if (!adminUser.result?.length || !marcUser.result?.length) {
                return 'missing users';
            }
            const adminPartnerId = adminUser.result[0].partner_id[0];
            const marcPartnerId = marcUser.result[0].partner_id[0];
            const createRes = await callKw({
                model: 'discuss.channel',
                method: 'create',
                args: [[{
                    name: 'Ops Escalations Blue',
                    channel_type: 'group',
                    channel_member_ids: [
                        [0, 0, { partner_id: adminPartnerId }],
                        [0, 0, { partner_id: marcPartnerId }],
                    ],
                }]],
                kwargs: {},
            });
            const channelId = Array.isArray(createRes.result) ? createRes.result[0] : createRes.result;
            const postRes = await callKw({
                model: 'mail.message',
                method: 'create',
                args: [[{
                    model: 'discuss.channel',
                    res_id: channelId,
                    body: 'Please triage the warehouse printer alerts before 4 PM.',
                    message_type: 'comment',
                    subtype_id: false,
                }]],
                kwargs: {},
            });
            const messageId = Array.isArray(postRes.result) ? postRes.result[0] : postRes.result;
            await callKw({
                model: 'discuss.channel',
                method: 'set_message_pin',
                args: [[channelId], messageId, true],
                kwargs: {},
            });
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
