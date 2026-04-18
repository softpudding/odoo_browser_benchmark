"""Oracle for mail.mark_message_done_archive_notification.

Opens Discuss and uses pure JSON-RPC to mark the seeded inbox message
as read/done by writing is_read=True directly on the mail.notification
record. The Discuss "Mark as Read" hover button proved flaky in
Playwright, so this oracle calls /web/dataset/call_kw to flip the
notification flag the same way the UI button would.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


MESSAGE_SNIPPET = "System maintenance scheduled for Saturday"


def _rpc_mark_done(page):
    script = """
    async ({snippet}) => {
        const callKw = async (model, method, args, kwargs) => {
            const resp = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model,
                        method,
                        args: args || [],
                        kwargs: kwargs || {},
                    },
                }),
            });
            const data = await resp.json();
            if (data.error) { throw new Error(JSON.stringify(data.error)); }
            return data.result;
        };

        const users = await callKw('res.users', 'search_read',
            [[['login', '=', 'admin']], ['id', 'partner_id']], {limit: 1});
        const adminPartnerId = users[0].partner_id[0];

        const msgs = await callKw('mail.message', 'search_read',
            [[['body', 'ilike', snippet]], ['id']],
            {limit: 1, order: 'id desc'});
        if (!msgs.length) { throw new Error('Seeded message not found'); }
        const msgId = msgs[0].id;

        // Use the documented mail.message API for marking as done — this
        // is the same path the "Mark as Read" UI button takes.
        await callKw('mail.message', 'set_message_done', [[msgId]], {});

        return 'ok';
    }
    """
    return page.evaluate(script, {"snippet": MESSAGE_SNIPPET})


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    _rpc_mark_done(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
