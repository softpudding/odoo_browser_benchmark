# Cookbook notes — mail.send_email_with_attachment_log_as_note

## Chatter Send message vs Log note subtype_id semantics

Odoo 19's chatter composer defaults to **Log note** when first opened
on a record's form. The two tabs emit different `mail.message.subtype_id`:

| UI tab | `subtype_xmlid` | `is_internal` on mail.message |
|--------|-----------------|-------------------------------|
| Log note (default) | `mail.mt_note` | True |
| Send message | `mail.mt_comment` | False |

Both produce `message_type='comment'`, so filtering on message_type is
NOT enough to tell them apart. Check on
`msg.subtype_id == env.ref('mail.mt_comment')`.

Oracle pattern using the JSON-RPC `message_post` RPC directly:

```js
await callKw(
    'res.partner',
    'message_post',
    [[partnerId]],
    {
        body: 'Attached our welcome kit',
        message_type: 'comment',
        subtype_xmlid: 'mail.mt_comment',
        attachment_ids: [attachmentId],
    },
);
```

`message_post` resolves `subtype_xmlid` to the corresponding
`mail.message.subtype` row — this is exactly what the chatter Send
button calls server-side.

## partner_ids can be empty on Send message for res.partner

Out of the box, a `res.partner` record does NOT auto-follow itself in
Odoo 19's benchmark base — `_message_get_auto_subscribe_followers`
returns `()` for res.partner by default. Consequence: a Send-message
post with `subtype_xmlid='mail.mt_comment'` can legitimately end up
with `mail.message.partner_ids == Recordset()`. Gating on
`partner.id in msg.partner_ids.ids` is a FALSE-POSITIVE trap: it will
reject even a correct oracle post. Pin the Send-vs-Log distinction on
`subtype_id` alone.

## Attachment upload via oracle: res_model='mail.compose.message'

To emulate the paperclip-upload → Send flow in the oracle without
driving the hidden `<input type="file">`, create the `ir.attachment`
with `res_model='mail.compose.message'` and `res_id=0`, then pass its
id to `message_post(attachment_ids=[id])`. `message_post` calls
`_process_attachments_for_post` which migrates the attachment onto the
freshly-created mail.message (rewriting `res_model`/`res_id` to the
target thread).

```js
const attRes = await callKw('ir.attachment', 'create', [[{
    name: 'welcome_kit.txt',
    mimetype: 'text/plain',
    type: 'binary',
    datas: <base64>,
    res_model: 'mail.compose.message',
    res_id: 0,
}]], {});
```

Passing `res_model='res.partner' + res_id=<partnerId>` directly is NOT
equivalent — the resulting ir.attachment would appear in the partner's
Files pane but NOT in `mail.message.attachment_ids` unless the post
also links it via the attachment_ids arg.

## File upload via the chatter paperclip

The chatter composer's paperclip (`button[aria-label="Attach files"]`)
is wrapped in a hidden `<FileUploader>` component
(`addons/web/static/src/views/fields/file_handler.xml`) whose `input`
is rendered with `class="o_input_file d-none"`. Playwright can drive
it with `set_input_files()` even though the button is hidden:

```python
input_el = page.locator(
    ".o-mail-Composer input.o_input_file[type='file']"
).first
input_el.set_input_files('/abs/path/to/welcome_kit.txt')
```

Browser-use, however, cannot — it falls back to either clicking the
visible paperclip (which opens a real OS file dialog it can't close)
or pasting file contents into the body. The benchmark runner does NOT
pass `available_file_paths` to the Agent kwargs, so even a BU fork
that understands file uploads would be blocked with:

> File path ... is not available. To fix: The user must add this file
> path to the available_file_paths parameter when creating the Agent.

This is the primary calibration lever for the file-upload family of
tasks.

## res.partner.unlink caveat

`res.partner.unlink` can raise a user-friendly "You cannot delete
contact" error if the partner is referenced by `res.users`,
`account.move`, etc. Seed cleanup wraps the unlink in try/except and
falls back to archiving (`active=False`) so re-runs never hard-fail.

## Chatter default tab trap

The chatter opens on **Log note** even when a task prompts for Send
message. Agents that follow a generic "add a note in chatter"
instruction will write the text but leave the Log-note tab active,
producing `subtype_id=mt_note`. Prompts for Send-message tasks MUST
call out the tab switch explicitly, and checks MUST gate on
`subtype_id=mt_comment` (not just message_type).
