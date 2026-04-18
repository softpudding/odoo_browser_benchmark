"""Oracle for mail.invite_external_email_to_existing_channel.

Mirror what the Discuss Invite People side panel does under the hood when
the user types a full email address, picks the envelope 'email fallback'
row, and clicks 'Invite to Group Chat'. Internally the Owl component
calls `discuss.channel.invite_by_email(channel_id, emails=[...])`, which
creates a mail.mail targeting the external address plus a
user_notification mail.message on the channel.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


CHANNEL_NAME = "project-discussion"
EXTERNAL_EMAIL = "external-guest@bench.test"


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    response = page.evaluate(
        """async ({channelName, email}) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                return res.json();
            };
            const chanRes = await callKw({
                model: 'discuss.channel',
                method: 'search_read',
                args: [[['name', '=', channelName]], ['id', 'name', 'channel_type']],
                kwargs: { limit: 1 },
            });
            if (!chanRes.result?.length) {
                return 'channel not found';
            }
            const channelId = chanRes.result[0].id;
            const inviteRes = await callKw({
                model: 'discuss.channel',
                method: 'invite_by_email',
                args: [[channelId]],
                kwargs: { emails: [email] },
            });
            if (inviteRes.error) {
                return 'invite failed: ' + JSON.stringify(inviteRes.error);
            }
            return 'ok';
        }""",
        {"channelName": CHANNEL_NAME, "email": EXTERNAL_EMAIL},
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
