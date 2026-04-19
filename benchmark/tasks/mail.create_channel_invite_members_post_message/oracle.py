"""Oracle for mail.create_channel_invite_members_post_message.

Open Discuss, then:
  1. Create the public 'team-bench' channel via JSON-RPC with
     channel_type='channel' and both bench users as members.
  2. Post 'Welcome team!' as a message_post on the channel.
This mirrors what the Discuss '+ Channels' button + Invite People side
panel + composer Enter does under the hood.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


CHANNEL_NAME = "team-bench"
WELCOME_MESSAGE = "Welcome team!"


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    response = page.evaluate(
        """async ({channelName, message}) => {
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
            const inviteeUsers = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [
                    [['login', 'in', ['bench_alice', 'bench_bob']]],
                    ['partner_id'],
                ],
                kwargs: {},
            });
            if (!adminUser.result?.length || inviteeUsers.result?.length !== 2) {
                return 'missing users (admin/bench_alice/bench_bob)';
            }
            const adminPartnerId = adminUser.result[0].partner_id[0];
            const partnerIds = inviteeUsers.result.map(u => u.partner_id[0]);

            const createRes = await callKw({
                model: 'discuss.channel',
                method: 'create',
                args: [[{
                    name: channelName,
                    channel_type: 'channel',
                    channel_member_ids: [
                        [0, 0, { partner_id: adminPartnerId }],
                        ...partnerIds.map(pid => [0, 0, { partner_id: pid }]),
                    ],
                }]],
                kwargs: {},
            });
            if (createRes.error) {
                return 'create failed: ' + JSON.stringify(createRes.error);
            }
            const channelId = Array.isArray(createRes.result)
                ? createRes.result[0]
                : createRes.result;
            if (!channelId) {
                return 'no channel id returned: ' + JSON.stringify(createRes.result);
            }

            const postRes = await callKw({
                model: 'discuss.channel',
                method: 'message_post',
                args: [[channelId]],
                kwargs: {
                    body: message,
                    message_type: 'comment',
                    subtype_xmlid: 'mail.mt_comment',
                },
            });
            if (postRes.error) {
                return 'message_post failed: ' + JSON.stringify(postRes.error);
            }
            return 'ok';
        }""",
        {"channelName": CHANNEL_NAME, "message": WELCOME_MESSAGE},
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
