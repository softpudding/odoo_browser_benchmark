"""Oracle for im_livechat.configure_channel_then_handle_widget_chat.

Uses JSON-RPC from an authenticated browser context to:
 1. Create the Bench Support live chat channel with admin as operator and
    the required welcome message.
 2. Create the :hi canned response authorised for the Live Chat user group
    (so it is available to the channel's operators in the discuss widget).
 3. Confirm that the channel's public support widget page loads, which is
    the simplest reliably verifiable state for the widget without needing
    a real websocket chat exchange.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/livechat")

    response = page.evaluate(
        """async () => {
            const unwrapId = (v) => Array.isArray(v) ? v[0] : v;
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

            // Locate the Administrator user (base.user_admin).
            const adminRes = await callKw({
                model: 'res.users',
                method: 'search_read',
                args: [[['login', '=', 'admin']], ['id', 'name']],
                kwargs: { limit: 1 },
            });
            if (!adminRes.length) {
                throw new Error('Administrator user missing');
            }
            const adminId = adminRes[0].id;

            // Locate the Live Chat user group so canned responses are shared
            // with the channel's operators.
            const groupRes = await callKw({
                model: 'ir.model.data',
                method: 'check_object_reference',
                args: ['im_livechat', 'im_livechat_group_user'],
                kwargs: {},
            });
            const livechatGroupId = Array.isArray(groupRes) ? groupRes[1] : groupRes;

            // Create the live chat channel with the exact configuration.
            const channelId = unwrapId(await callKw({
                model: 'im_livechat.channel',
                method: 'create',
                args: [[{
                    name: 'Bench Support',
                    default_message: 'How can we help?',
                    user_ids: [[6, 0, [adminId]]],
                }]],
                kwargs: {},
            }));

            // Create the canned response used by this channel's operators.
            await callKw({
                model: 'mail.canned.response',
                method: 'create',
                args: [[{
                    source: ':hi',
                    substitution: 'Hi! How can I help you today?',
                    group_ids: [[6, 0, [livechatGroupId]]],
                }]],
                kwargs: {},
            });

            // Verify the channel stored the right configuration.
            const channelAfter = await callKw({
                model: 'im_livechat.channel',
                method: 'read',
                args: [[channelId], ['name', 'default_message', 'user_ids', 'web_page']],
                kwargs: {},
            });
            if (!channelAfter || !channelAfter[0]) {
                throw new Error('channel read failed');
            }
            const rec = channelAfter[0];
            if (rec.name !== 'Bench Support') {
                throw new Error('channel name mismatch: ' + rec.name);
            }
            if (rec.default_message !== 'How can we help?') {
                throw new Error('welcome message mismatch: ' + rec.default_message);
            }
            if (!rec.user_ids || rec.user_ids.indexOf(adminId) === -1) {
                throw new Error('admin operator missing on channel');
            }

            // Load the public support widget page to confirm it is served
            // and renders the welcome message we configured.
            const supportRes = await fetch(`/im_livechat/support/${channelId}`, {
                credentials: 'same-origin',
            });
            if (!supportRes.ok) {
                throw new Error('support page not reachable: ' + supportRes.status);
            }
            const html = await supportRes.text();
            if (html.indexOf('How can we help?') === -1) {
                // The welcome message is loaded via JS from get_livechat_info,
                // so fall back to verifying that through the backend.
                const infoRes = await callKw({
                    model: 'im_livechat.channel',
                    method: 'get_livechat_info',
                    args: [[channelId]],
                    kwargs: {},
                });
                const message = infoRes && infoRes.options
                    ? infoRes.options.default_message
                    : null;
                if (message !== 'How can we help?') {
                    throw new Error(
                        'widget welcome message mismatch: ' + JSON.stringify(infoRes)
                    );
                }
            }

            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
