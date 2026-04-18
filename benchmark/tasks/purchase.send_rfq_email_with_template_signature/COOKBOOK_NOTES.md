# purchase.send_rfq_email_with_template_signature — Odoo 19 cookbook

## Purchase RFQ Send: button label & template surprises

- Header button on `purchase.order` in `state='draft'` is **`Send RFQ`**
  (NOT "Send by Email"). On `state='purchase'` it's **`Send PO`**. The
  underlying server method is the same — `action_rfq_send` — with
  `context={'send_rfq': True|False}` to pick the template.
- `action_rfq_send` passes `default_template_id` into the compose wizard
  context. The three pre-installed `mail.template` records on
  `purchase.order` are:
  - `purchase.email_template_edi_purchase` — **Purchase: Request For
    Quotation** (loaded by default when `send_rfq=True` / state=draft)
  - `purchase.email_template_edi_purchase_done` — **Purchase: Purchase
    Order** (default when `send_rfq=False` / state=purchase)
  - `purchase.email_template_edi_purchase_reminder` — **Purchase: Vendor
    Reminder** (used by the reminder cron, has a separate
    `email_from` pin)
- `action_rfq_send` sets `mark_rfq_as_sent=True` in the context, so the
  mail.compose.message → `_notify_thread` → purchase override flips any
  still-draft PO to `state='sent'` as a side effect of the send.
- `use_default_to=True` on these templates means `partner_ids` is left
  empty in the wizard; recipients resolve at send-time from the thread's
  `_notify_get_default_recipients`. The view still enables the primary
  **Send** button via `partner_ids_all_have_email` — which is vacuously
  True (`all([]) == True`) when `partner_ids` is empty.

## wkhtmltopdf trap: RFQ/PO mail templates attach a PDF report

Both the RFQ and PO mail templates ship with
`report_template_ids=[purchase.report_purchase_quotation]` /
`[purchase.action_report_purchase_order]`. `mail.template.send_mail`
renders the report synchronously when the compose wizard opens (to
generate an attachment), which requires **wkhtmltopdf**. On benchmark
runners wkhtmltopdf is **not installed** — a modal dialog "Invalid
Operation — Unable to find Wkhtmltopdf on this system. The PDF can not
be created." pops instead of the compose wizard.

Seed fix:

```python
for xml_id in ("purchase.email_template_edi_purchase",
               "purchase.email_template_edi_purchase_done"):
    tpl = env.ref(xml_id, raise_if_not_found=False)
    if tpl and tpl.report_template_ids:
        tpl.write({"report_template_ids": [(5, 0, 0)]})
```

Detaching the reports makes the wizard open immediately; the sent mail
simply has no PDF attachment. All state transitions still fire (state →
sent, mail.message logged, mail.mail created and sent via the SMTP sink).

## mail.compose.message body editor: pointer intercept from .o_technical_modal

The compose dialog renders inside `<div class="modal d-block
o_technical_modal">`. The HTML editor's inner `contenteditable` is laid
out with transparent padding that the modal wrapper captures. A plain
Playwright `body.click()` hits the modal overlay and retries 100+ times
for 60s before timing out (reported as
`<div ... class="modal d-block o_technical_modal">...</div> subtree
intercepts pointer events`).

Pattern that works: skip the click entirely, focus the editable via
JS, and place the caret with a DOM Range:

```python
body.evaluate("""el => {
    el.focus();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);   // caret at END
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}""")
page.keyboard.press("Enter"); page.keyboard.press("Enter")
page.keyboard.insert_text("Please confirm by Friday.")
```

## mail_composer_template_selector widget: no visible `<select>`

The `mail_composer_template_selector` widget renders as a single
ellipsis-v icon button with `title="Templates"` and class
`.mail-composer-template-dropdown-btn`. Clicking it opens an Owl
`<Dropdown>` whose menu is *portaled OUT of the modal* into a
page-level container `.mail-composer-template-dropdown`. So when
scoped to `modal.locator(...)`, the dropdown items are NOT found.

Working selectors:

```python
modal.locator(".mail-composer-template-dropdown-btn").click()
page.locator(
    ".mail-composer-template-dropdown .dropdown-item:has-text('...')"
).first.click()
# Fallback: ".dropdown-menu:visible .dropdown-item:has-text('...')"
```

After `onLoadTemplate` runs, the body editor node is re-mounted, so any
previously-acquired `body` locator becomes detached. Re-query the body
AFTER the template switch.

## Wizard footer Send button: primary vs disabled twin

`mail_compose_message_views.xml` defines TWO Send buttons in the footer:
one enabled (`invisible="... or not partner_ids_all_have_email"`) and one
disabled (`disabled="1"`, `invisible="... or partner_ids_all_have_email"`).
Both have `class="btn-primary o_mail_send"` and visible text "Send".

A naive `button:has-text('Send')` matches the disabled twin and times
out on click. Use:

```python
modal.locator("button.o_mail_send:not([disabled]):visible").first
```

## Message-type filter for distractor leak-check

An auto-generated `mail.message` posting ("RFQ Sent") is always logged
against the target PO when `action_rfq_send` fires (even with no body
custom content), so `search_count(model, res_id)` is NOT a reliable
"did the distractor receive an outgoing mail?" check. Filter by
`message_type='email_outgoing'` to pick up only the actual sent emails,
not internal state-change notifications.
