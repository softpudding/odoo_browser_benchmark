"""Oracle for mail.send_email_with_attachment_log_as_note.

Reproduces what the Odoo chatter 'Send message' action does under the
hood when the user types a body, paperclip-uploads an attachment, and
clicks Send:

  1. Upload the file via /mail/attachment/upload (the same endpoint the
     paperclip uses) so the attachment_id is registered as a 'pending'
     composer attachment — this is equivalent to the agent picking a
     file in the OS file dialog.
  2. Call res.partner.message_post with body + attachment_ids,
     message_type='comment', subtype_xmlid='mail.mt_comment' (the
     subtype 'Send message' uses by default). This creates the
     mail.message with the attachment linked and partner_ids populated
     (Send-message notifies followers, including the record partner).

Browser-use on the same task fails because (a) the chatter opens on
Log note by default (subtype=mail.mt_note) so its post fails the
subtype check, and (b) the paperclip triggers a hidden
<input type=file> that needs an OS file dialog that BU cannot drive
and that the benchmark runner does not whitelist via
`available_file_paths`.
"""

import base64
import os

from benchmark.oracle_helpers import login, navigate, run_oracle


PARTNER_NAME = "Bench Chatter Co"
EXPECTED_BODY = "Attached our welcome kit"
ATTACHMENT_FILENAME = "welcome_kit.txt"

ATTACHMENT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "seed_artifacts",
    ATTACHMENT_FILENAME,
)


def oracle(page):
    login(page)
    # Landing on a live Odoo view first so the session cookie + CSRF
    # token for /mail/attachment/upload are initialised.
    navigate(page, "/odoo/contacts")

    with open(ATTACHMENT_PATH, "rb") as f:
        body_b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "partner_name": PARTNER_NAME,
        "body": EXPECTED_BODY,
        "attachment_name": ATTACHMENT_FILENAME,
        "attachment_b64": body_b64,
        "mimetype": "text/plain",
    }

    response = page.evaluate(
        """async (payload) => {
            const callKw = async (model, method, args, kwargs) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: { model, method, args, kwargs: kwargs || {} },
                    }),
                });
                const j = await res.json();
                if (j.error) {
                    throw new Error(JSON.stringify(j.error));
                }
                return j.result;
            };

            // 1. Resolve the target partner.
            const rows = await callKw(
                'res.partner',
                'search_read',
                [[['name', '=', payload.partner_name]], ['id', 'name']],
                { limit: 1 },
            );
            if (!rows || !rows.length) {
                throw new Error('Seeded partner not found: ' + payload.partner_name);
            }
            const partnerId = rows[0].id;

            // 2. Create the ir.attachment directly as a mail attachment
            // (res_model/res_id left empty so message_post can migrate
            // it onto the freshly-created mail.message — this is what
            // Odoo 19's _process_attachments_for_post does under the
            // hood).
            const attRes = await callKw(
                'ir.attachment',
                'create',
                [[{
                    name: payload.attachment_name,
                    mimetype: payload.mimetype,
                    type: 'binary',
                    datas: payload.attachment_b64,
                    res_model: 'mail.compose.message',
                    res_id: 0,
                }]],
                {},
            );
            const attachmentId = Array.isArray(attRes) ? attRes[0] : attRes;

            // 3. message_post on the partner with subtype_xmlid
            // 'mail.mt_comment' (the Send-message subtype). This is
            // exactly what the chatter Send button does.
            await callKw(
                'res.partner',
                'message_post',
                [[partnerId]],
                {
                    body: payload.body,
                    message_type: 'comment',
                    subtype_xmlid: 'mail.mt_comment',
                    attachment_ids: [attachmentId],
                },
            );

            return 'ok';
        }""",
        payload,
    )

    if response != "ok":
        raise RuntimeError(f"Unexpected oracle response: {response!r}")


run_oracle(oracle)
