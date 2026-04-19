# account.print_invoice_pdf_attach_to_partner — Odoo 19 cookbook

## Task summary

Row 495, hard tier-3. Seed a POSTED customer invoice `BENCH-PRINT-001`
(Bench Print Co / 150.00, 1 line). Agent opens the invoice, clicks the
header **Send**, and in the Send & Print wizard clicks the primary
**Send** button. The wizard posts a `mail.message` on the invoice whose
`attachment_ids` include the pre-seeded invoice PDF (filename ending
`.pdf`, mimetype `application/pdf`).

Distinct from **row 446** (`account.post_draft_invoice_send_to_customer`)
which asserts only a `mail.message` exists on the chatter — row 495
explicitly asserts the PDF attachment on that message. Both share the
same wkhtmltopdf workaround.

## Key file references

- Wizard model: `addons/account/wizard/account_move_send_wizard.py`
- Wizard view: `addons/account/wizard/account_move_send_wizard.xml`
- Invoice header buttons: `addons/account/views/account_move_views.xml`
  (look for `action_invoice_sent` (Send) and `action_print_pdf` (Print)).
- Send mechanics: `addons/account/models/account_move_send.py`
  (`_generate_and_send_invoices`, `_hook_if_success`, `_send_mails`,
  `_send_mail`, `_get_mail_params`, `_get_invoice_extra_attachments`).
- Invoice PDF binary field: `addons/account/models/account_move.py`
  (`invoice_pdf_report_file` + `invoice_pdf_report_id`
  computed-Many2one via `_compute_linked_attachment_id`).

## Where the PDF attachment actually comes from

With the stub-PDF workaround (seed writes `invoice_pdf_report_file`
before the run), `account.move.send._send_mails` calls `_send_mail`,
which in turn calls `message_post(attachments=[(pdf_name, pdf_raw)])`.

The `attachments` list is built in `_get_mail_params`:

```python
for attachment_data in self._get_invoice_extra_attachments_data(move) + mail_attachments_widget:
    ...
mail_attachments = [
    (attachment.name, attachment.raw)
    for attachment in self.env['ir.attachment'].browse(list(seen_attachment_ids)).exists()
]
```

`_get_invoice_extra_attachments(move)` returns `move.invoice_pdf_report_id`
(the seeded stub). That attachment's `.name` is the field name
`invoice_pdf_report_file` (NOT `.pdf`-suffixed), but its `.raw` is the
raw PDF bytes and its `.mimetype` is `application/pdf` (auto-detected
by `ir.attachment._compute_mimetype` from the `%PDF-1.4\n…` header).

In `_process_attachments_for_post` (mail.thread), the tuple `(name,
content)` is written into a NEW `ir.attachment` with
`name=<attachment.name>`. Good news: when this new attachment is
finally downloaded via the chatter widget's file link, the web
controller appends a `.pdf` extension to the filename based on the
mimetype — so downloaded file lands as `invoice_pdf_report_file.pdf`.

## Check strategy: filename-OR-mimetype

Because the in-DB `ir.attachment.name` for the seeded extra-attachment
is `'invoice_pdf_report_file'` (no `.pdf` suffix), check.py must accept
EITHER:
- filename ending in `.pdf`, OR
- `mimetype == 'application/pdf'`

`_attachment_is_pdf(att)` implements exactly this. Gating only on
filename ending `.pdf` would spuriously fail — the inner attachment's
`.name` is the field name verbatim. Gating only on mimetype works in
practice but is tighter to verify via downloaded artifacts.

## Why wkhtmltopdf absence does NOT break the flow

Seed writes `invoice_pdf_report_file = base64(<valid PDF bytes>)`
BEFORE the agent runs. `invoice_pdf_report_id` is a computed Many2one
backed by the `res_model='account.move', res_field='invoice_pdf_report_file'`
attachment rows, so it resolves to truthy. In
`_generate_invoice_documents`:

```python
if not invoice_data.get('error') and not invoice.invoice_pdf_report_id:
    pdf_to_generate[invoice] = invoice_data
```

the guard skips the wkhtml render path, `pdf_to_generate` is empty,
`_pre_render_qweb_pdf` is never called, no wkhtmltopdf invocation
occurs. `_hook_if_success` still runs `_send_mails`, which is the
code path that produces the chatter `mail.message` + PDF attachment.

## Header buttons gotcha (trap for the agent)

The posted out_invoice header has THREE Print/Send buttons:

1. **Send** (`action_invoice_sent`): opens Send & Print wizard → calls
   `_send_mails` → posts mail.message with PDF on chatter. ✓ TASK PATH.
2. **Print** (highlighted, visible only when `not is_being_sent and
   not invoice_pdf_report_id`): calls `action_print_pdf` which returns
   an `ir.actions.report`, triggering wkhtmltopdf. ✗ FAILS (no wkhtml).
3. **Print** (non-highlighted, visible when `is_being_sent or
   invoice_pdf_report_id`): same `action_print_pdf` handler — also
   triggers wkhtml. ✗ FAILS.

Because the seed pre-fills `invoice_pdf_report_file`, the SECOND Print
button (non-highlighted) is the one the agent sees. The `Send` button
on our seed is also non-highlighted (`is_move_sent` is still False,
but `invoice_pdf_report_id` is truthy — which flips
`highlight_send_button`? Let's check: the computation is
`highlight_send_button = not is_being_sent and not
invoice_pdf_report_id`). So highlight_send_button=False here too. Both
Send and Print are non-highlighted in this seed. The Send button is
therefore not visually pre-selected — the agent has to read labels
carefully.

## sending_method_checkboxes: only "by Email" on the base snapshot

The wizard's `sending_method_checkboxes` widget renders one checkbox
per method in `res.partner.invoice_sending_method.selection`, minus
'manual'. The base snapshot has `[('manual', 'Manual'), ('email', 'by
Email')]` — after manual is filtered out, only `Email` remains.
`snailmail_account` adds `('snailmail', 'by Post')` (NOT enabled in
the benchmark base). There is NO "by Print" checkbox in this wizard
on the base snapshot, contrary to what some Odoo Enterprise screenshots
might suggest. The prompt therefore does NOT ask the agent to tick
a Print checkbox — just to click the primary Send button.

## base_document_layout configurator pre-wizard

As with row 446: seed pre-sets `company.external_report_layout_id =
web.external_layout_standard` so clicking Send does NOT pop the
`base.document_layout` configurator before the send wizard. Without
this, the agent sees an unexpected layout-picker dialog first. The
oracle also defensively dismisses the layout dialog if it appears.

## Oracle minimal path

Open `/odoo/accounting/customer-invoices` → `clear_search_filters` →
`search_for('BENCH-PRINT-001')` → `click_list_row('BENCH-PRINT-001')`
→ `click_status_button('Send')` → wait → click
`modal.btn-primary[name='action_send_and_print']`. No checkbox
manipulation needed.

Oracle PASS: F1=1.0, 40.0s wall clock, 0 postcondition failures,
46 API calls (17 writes, 29 reads), 0 forbidden ops, StrictClean=True.

## Browser-Use calibration MISS — task is NOT hard

**Browser-Use single-shot PASSED** in 11 steps / 87.0s. Steps taken:
navigate → login → wait → click invoice row → click header Send →
click primary Send in wizard → extract chatter to verify PDF → extra
verification via eval() and download → done. Final download confirmed
the attachment saved as `invoice_pdf_report_file.pdf` (143 bytes,
matching the stub PDF).

Why BU passes so easily:
- The Send dialog is completely pre-populated (To, Subject, Body,
  Email checkbox all defaulted). There is no decision point.
- The primary footer button is unambiguously labelled "Send" —
  there is no "Send & Print" alternative button or non-default
  sending method to pick (manual is filtered; Post requires
  snailmail_account which is off).
- The chatter refreshes immediately after wizard close and the
  attachment icon is obvious.

**To re-harden into a genuine hard pattern (~40% pass)** would need
one or more of:

1. Require **unchecking Email** and explicitly attaching the PDF via
   the paperclip on a Log-note / Send-message chatter action (OS file
   picker friction — see row 434 pattern). But the PDF can't be
   downloaded first without wkhtmltopdf, so this requires agent to
   manually upload a different file.
2. Add an **extra_edi** Peppol / UBL step that requires the agent to
   un-tick / tick a secondary checkbox before Send.
3. Require an **additional recipient** via the `To` many-to-many
   tag picker (pattern from row 49 `send_invoice_with_extra_recipient`
   which combines this with the same Send wizard and which DID produce
   a calibration hit in practice).
4. Seed a near-duplicate invoice `BENCH-PRINT-002` for a different
   partner as a distractor so the agent has to disambiguate before
   Send — but row 49's BU pass shows BU can do distractors here.
5. Move the attach-point check off mail.message to a specific
   chatter-attachment slot (e.g. `message_main_attachment_id`) that
   only flips after proper Send & Print dispatch — but that slot IS
   set by `_link_invoice_documents` only when new pdf_attachment_values
   are generated, which with the stub-PDF workaround never happens.
6. Pre-seed the invoice WITHOUT the stub PDF (remove the wkhtml
   workaround) and accept that wkhtmltopdf-absent environments will
   uniformly fail. Task becomes BLOCKED on this env.

Kept as hard / tier-3 / primary_track for now because it exercises a
distinct check (PDF attachment on chatter, not just mail.message
existence) and the cookbook knowledge (the seed-stub pattern, the
header Print vs Send branch) is useful for downstream tasks.

## Quirks worth remembering (cookbook deltas vs row 446)

- (NEW) The seeded `invoice_pdf_report_file` attachment carries the
  PDF through the Send path and surfaces on the chatter, BUT its
  `.name` is `invoice_pdf_report_file` verbatim (no `.pdf` suffix),
  so check.py must allow `mimetype=application/pdf` as an alternate
  gate — filename-only gating spuriously fails.
- (NEW) The `Print` header button (`action_print_pdf`) is orthogonal
  to the chatter-attach path: it returns an `ir.actions.report`, runs
  wkhtmltopdf, and produces no mail.message. Prompts that conflate
  "Print the PDF" with "attach to chatter" confuse browser agents —
  prompt explicitly explains that the chatter-attach happens via
  **Send**, not **Print**.
- (REUSED from row 446) Same wkhtmltopdf-stub workaround; same
  `external_report_layout_id` pre-set to bypass layout configurator.

## Commit

`[ADD] benchmark: account.print_invoice_pdf_attach_to_partner (hard)`.
Calibration hit: NO (BU PASS single-shot, F1=1.0). Retained as
`difficulty=hard`, `tier=3`, `primary_track=true` because the check
distinguishes it from row 446 and the cookbook captures new
downstream knowledge.
