"""Oracle for mail.create_channel_invite_members.

Open Discuss, then create a private group channel with the two invitees
via Odoo's JSON-RPC API. This mirrors what the Discuss "New Channel" /
"Add Members" UI does under the hood.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


CHANNEL_NAME = "Release Rehearsal Team"


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
            const nadiaUser = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['name', '=', 'Nadia Rossi']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            const oliverUser = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['name', '=', 'Oliver Chen']], ['partner_id']],
                kwargs: { limit: 1 },
            });
            if (!adminUser.result?.length || !nadiaUser.result?.length || !oliverUser.result?.length) {
                return 'missing users';
            }
            const adminPartnerId = adminUser.result[0].partner_id[0];
            const nadiaPartnerId = nadiaUser.result[0].partner_id[0];
            const oliverPartnerId = oliverUser.result[0].partner_id[0];

            const createRes = await callKw({
                model: 'discuss.channel',
                method: 'create',
                args: [[{
                    name: 'Release Rehearsal Team',
                    channel_type: 'group',
                    channel_member_ids: [
                        [0, 0, { partner_id: adminPartnerId }],
                        [0, 0, { partner_id: nadiaPartnerId }],
                        [0, 0, { partner_id: oliverPartnerId }],
                    ],
                }]],
                kwargs: {},
            });
            if (createRes.error) {
                return 'create failed: ' + JSON.stringify(createRes.error);
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
