"""Oracle for im_livechat.configure_offline_form_and_test_widget."""

from benchmark.oracle_helpers import login, navigate, run_oracle


def oracle(page):
    login(page)
    navigate(page, "/odoo/livechat")
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

            const channelId = unwrapId(await callKw({
                model: 'im_livechat.channel',
                method: 'create',
                args: [[{
                    name: 'After Hours Help',
                    button_text: 'Questions after hours?',
                    default_message: 'Leave your email and we will get back to you tomorrow morning.',
                }]],
                kwargs: {},
            }));
            const supportRes = await fetch(`/im_livechat/support/${channelId}`, { credentials: 'same-origin' });
            if (!supportRes.ok) {
                throw new Error('support page not reachable');
            }
            return 'ok';
        }""",
    )
    if response != "ok":
        raise RuntimeError(response)


run_oracle(oracle)
