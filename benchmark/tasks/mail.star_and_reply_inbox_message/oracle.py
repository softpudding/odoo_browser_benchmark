"""Oracle for mail.star_and_reply_inbox_message.

Navigates to the Discuss Inbox and uses pure JSON-RPC to star the seeded
message and post a reply. UI Playwright interactions in the Discuss
panel proved flaky (composer focus / send button visibility), so this
oracle calls /web/dataset/call_kw directly. The browser context is
authenticated, so cookies and CSRF are valid.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)

SEEDED_SUBJECT = "Q2 status update - confirmation needed"
REPLY_BODY = "Acknowledged - will follow up by Friday."


def _rpc_star_and_reply(page):
    script = """
    async ({replyBody, seededSubject}) => {
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
            [[['subject', '=', seededSubject]],
             ['id', 'model', 'res_id', 'starred_partner_ids']],
            {limit: 1, order: 'id desc'});
        if (!msgs.length) { throw new Error('Seeded message not found'); }
        const msg = msgs[0];

        // Only toggle if not already starred for admin.
        const isStarred = (msg.starred_partner_ids || []).includes(adminPartnerId);
        if (!isStarred) {
            await callKw('mail.message', 'toggle_message_starred',
                [[msg.id]], {});
        }

        // message_post on the parent thread is the supported path; it
        // persists body + author and links via parent_id correctly.
        await callKw(msg.model, 'message_post',
            [[msg.res_id]],
            {
                body: '<p>' + replyBody + '</p>',
                message_type: 'comment',
                subtype_xmlid: 'mail.mt_comment',
                parent_id: msg.id,
                author_id: adminPartnerId,
            });

        return 'ok';
    }
    """
    return page.evaluate(
        script,
        {
            "replyBody": REPLY_BODY,
            "seededSubject": SEEDED_SUBJECT,
        },
    )


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    _rpc_star_and_reply(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
