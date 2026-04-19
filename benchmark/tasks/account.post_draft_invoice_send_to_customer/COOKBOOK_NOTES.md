# account.post_draft_invoice_send_to_customer — Odoo 19 cookbook

## Header & wizard buttons on `account.move`

- Posted `out_invoice` header renders `<button name="action_invoice_sent"
  string="Send"/>`. The button label is **"Send"** — NOT "Send & Print".
  It is highlighted (`oe_highlight`) when `display_send_button=True AND
  highlight_send_button=True`, i.e. `is_move_sent=False AND not
  is_being_sent`.
- `account.move.send.wizard` footer (see
  `addons/account/wizard/account_move_send_wizard.xml`):
  - **Primary** `<button string="Send" name="action_send_and_print"
    class="btn-primary" invisible="not sending_methods"/>` — the
    button label switches to `Generate` when no sending methods are
    selected. `action_send_and_print` is the server method; the UI
    label is just "Send".
  - **Secondary** `<button string="Discard" special="cancel"
    class="btn-secondary"/>` — agent must NOT click this.
- Defaults: `_compute_sending_method_checkboxes` pre-checks **email**
  based on the partner's `invoice_sending_method`; `_compute_mail_partners`
  pre-fills **To** with the commercial partner when it has an email.
  `_compute_template_id` picks the template from
  `invoice_template_pdf_report_id` / `mail_template_id`.

## wkhtmltopdf trap: the account.move.send PDF step

The account Send wizard runs `_prepare_invoice_pdf_report` →
`ir.actions.report._pre_render_qweb_pdf`, which shells out to
**wkhtmltopdf**. The benchmark environment does NOT have wkhtmltopdf
installed. Without the workaround below, `action_send_and_print`
raises a UserError ("Unable to find Wkhtmltopdf"), the wizard stays
open, no mail is sent, and `is_move_sent` never flips.

**Seed workaround**: pre-write a stub binary into
`invoice_pdf_report_file` so the computed `invoice_pdf_report_id`
resolves to an existing attachment and the wizard's PDF-generation
guard skips the wkhtmltopdf render path:

```python
import base64
invoice = env["account.move"].create({...})
stub_pdf = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
invoice.sudo().write({
    "invoice_pdf_report_file": base64.b64encode(stub_pdf),
})
```

The guard is in `_generate_invoice_documents`:

```python
if not invoice_data.get('error') and not invoice.invoice_pdf_report_id:
    pdf_to_generate[invoice] = invoice_data
```

This is distinct from the `purchase.send_rfq_email_with_template_signature`
workaround, which detaches `report_template_ids` from the mail template
(a different code path: `mail.template.send_mail` renders a report
attachment via its `report_template_ids`, not via
`_prepare_invoice_pdf_report`).

## `is_move_sent` does NOT flip with the wkhtmltopdf stub

With the stub-PDF workaround, `_prepare_invoice_pdf_report` is skipped,
which means `pdf_attachment_values` is never populated, which means
`_link_invoice_documents` returns early (no new attachments to create),
which means `invoice.is_move_sent = True` is never set.

However, `_hook_if_success` DOES run and calls `_send_mails`, which
posts a `mail.message` on the invoice with `message_type='comment'`,
`subtype_id=mail.mt_comment`, `body=<template-rendered body>`. So the
outbound email IS tracked on the chatter — just not via `is_move_sent`.

**check.py must gate on the `mail.message` (subtype = `mail.mt_comment`
and `message_type in ('email','comment','email_outgoing')`) or a
`mail.notification` with `notification_type='email'`, NOT on
`is_move_sent`.**

## base_document_layout configurator pre-wizard

`account.move.action_invoice_sent` wraps the send action in
`_get_action_with_base_document_layout_configurator`, which pops a
layout-picker dialog BEFORE the actual send wizard when:

```python
self.env.is_admin()
and not self.env.company.external_report_layout_id
and not self.env.context.get('discard_logo_check')
```

Seed must pre-set this to avoid the configurator:

```python
company = env.company
if not company.external_report_layout_id:
    layout = env.ref("web.external_layout_standard", raise_if_not_found=False)
    if layout:
        company.sudo().external_report_layout_id = layout.id
```

## Customers > Invoices list default filter

The Customers → Invoices list at
`/odoo/accounting/customer-invoices` is filtered by default to include
DRAFT + POSTED + CANCEL invoices (no state filter applied out of the
box). Still, with many seeded invoices the target may be off-screen;
using `search_for(ref)` in the oracle surfaces the draft reliably.
`click_list_row` then navigates to the form.

## Calibration: too easy for "medium"

Browser-Use single-shot PASS (F1=1.0, 74.3s). The dialog is completely
pre-populated — primary "Send" is the obvious click. To harden into a
genuine medium/hard, combine with one of:
- Require unchecking Email and checking **Post** (snailmail) instead.
- Require editing the Subject or body before clicking Send.
- Require adding an **extra recipient** (see
  `account.send_invoice_with_extra_recipient` for this exact pattern).
- Require **Save as Template** → name the template → then send.

## Key file references

- Wizard model: `addons/account/wizard/account_move_send_wizard.py`
- Wizard view: `addons/account/wizard/account_move_send_wizard.xml`
- Invoice header buttons: `addons/account/views/account_move_views.xml`
  (search for `action_invoice_sent`, `action_post`).
- Send mechanics: `addons/account/models/account_move_send.py`
  (`_generate_and_send_invoices`, `_hook_if_success`, `_send_mail`,
  `_link_invoice_documents`).
