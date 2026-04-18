"""Oracle for mail.create_group_channel_upload_attachment.

Opens Discuss and uses pure JSON-RPC (call_kw) to:
  1. Resolve admin + Bob partner ids.
  2. Create a 'group' discuss.channel named 'Bench Project Sync' with
     admin and Bob as members via channel_member_ids.
  3. Create an ir.attachment named 'sync-notes.txt' linked to that channel
     (res_model='discuss.channel', res_id=channel.id) with the seeded body.
  4. Post a mail.message on the channel that links the attachment so it
     appears in the channel as an uploaded file (mirrors the UI flow of
     attaching a file in the composer and pressing send).
"""

import base64

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


CHANNEL_NAME = "Bench Project Sync"
ATTACHMENT_NAME = "sync-notes.txt"
ATTACHMENT_BODY = "Kickoff agenda for Bench Project Sync."
BOB_EMAIL = "channel.bob@bench.test"


def _rpc_create_channel_and_attach(page):
    payload = {
        "channel_name": CHANNEL_NAME,
        "attachment_name": ATTACHMENT_NAME,
        "attachment_b64": base64.b64encode(
            ATTACHMENT_BODY.encode("utf-8")
        ).decode("ascii"),
        "bob_email": BOB_EMAIL,
    }
    script = """
    async (payload) => {
        const callKw = async (model, method, args, kwargs) => {
            const resp = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'same-origin',
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

        // Resolve admin and Bob partner ids.
        const adminUser = await callKw(
            'res.users', 'search_read',
            [[['login', '=', 'admin']], ['id', 'partner_id']],
            {limit: 1}
        );
        if (!adminUser.length) { throw new Error('Admin user missing'); }
        const adminPartnerId = adminUser[0].partner_id[0];

        const bobUser = await callKw(
            'res.users', 'search_read',
            [[['email', '=', payload.bob_email]], ['id', 'partner_id']],
            {limit: 1}
        );
        if (!bobUser.length) { throw new Error('Seeded Bob user not found'); }
        const bobPartnerId = bobUser[0].partner_id[0];

        // Create the private group channel with admin + Bob as members.
        const created = await callKw(
            'discuss.channel', 'create',
            [[{
                name: payload.channel_name,
                channel_type: 'group',
                channel_member_ids: [
                    [0, 0, {partner_id: adminPartnerId}],
                    [0, 0, {partner_id: bobPartnerId}],
                ],
            }]],
            {}
        );
        const channelId = Array.isArray(created) ? created[0] : created;

        // Create the ir.attachment linked to the channel. The composer's
        // upload step does the same: it POSTs to /mail/attachment/upload
        // which under the hood creates an ir.attachment with
        // res_model='discuss.channel' and res_id=<channel_id>.
        const attId = await callKw(
            'ir.attachment', 'create',
            [[{
                name: payload.attachment_name,
                res_model: 'discuss.channel',
                res_id: channelId,
                type: 'binary',
                mimetype: 'text/plain',
                datas: payload.attachment_b64,
            }]],
            {}
        );
        const attachmentId = Array.isArray(attId) ? attId[0] : attId;

        // Post a message on the channel linking the attachment so it
        // appears in the channel timeline (the UI's "Send" step).
        await callKw(
            'discuss.channel', 'message_post',
            [[channelId]],
            {
                body: '',
                message_type: 'comment',
                subtype_xmlid: 'mail.mt_comment',
                attachment_ids: [attachmentId],
                author_id: adminPartnerId,
            }
        );

        return 'ok';
    }
    """
    result = page.evaluate(script, payload)
    if result != "ok":
        raise RuntimeError(f"Unexpected oracle response: {result!r}")


def oracle(page):
    login(page)
    navigate(page, "/odoo/discuss")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    _rpc_create_channel_and_attach(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
