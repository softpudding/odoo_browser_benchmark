"""Seed for account.print_invoice_pdf_attach_to_partner.

Category: deep_ui_interaction (HARD).

Seeds a single POSTED customer invoice (out_invoice) for a seeded
partner with a service line totaling 150.00 (taxes cleared).

Agent must open the Send & Print wizard and tick the 'by Print'
checkbox in addition to the pre-ticked 'by Email', then click the
primary Send button. The Send flow then posts a mail.message on the
invoice with the PDF attached.

# wkhtmltopdf workaround (see row 446 COOKBOOK_NOTES)

This benchmark environment does NOT have wkhtmltopdf installed.
Without a workaround, `account.move.send._prepare_invoice_pdf_report`
shells out to wkhtmltopdf, raises UserError, the wizard stays open,
the mail is never sent and no PDF is attached.

We seed a stub `invoice_pdf_report_file` (valid-ish minimal PDF
bytes) BEFORE posting. Because `invoice_pdf_report_id` is a
computed many2one backed by the stored Binary attachment, this makes
`_generate_invoice_documents`'s guard
`if not invoice.invoice_pdf_report_id: pdf_to_generate[invoice] = ...`
fall through (no regeneration). `_hook_if_success` then runs
`_send_mails`, which calls `message_post(..., attachments=[(pdf_name,
pdf_raw)])` using `_get_invoice_extra_attachments(move) ==
move.invoice_pdf_report_id`, resulting in a mail.message with a
real-bytes PDF attachment on the invoice chatter.

# base_document_layout configurator

As in row 446, we pre-set `company.external_report_layout_id` to the
Standard layout so clicking Send does NOT pop the layout configurator
dialog before the send wizard.

# Why posted, not draft?

Row 495 specifically targets the *Print + attach* leg of the flow,
NOT the post step. The invoice is seeded already posted so the agent
can go straight to Send & Print without a Confirm step.
"""

import base64


TARGET_REF = "BENCH-PRINT-001"
PARTNER_NAME = "Bench Print Co"
PARTNER_EMAIL = "billing@benchprint.example.com"
PRODUCT_NAME = "Bench Print Service"


# Minimal but valid-looking single-page PDF. `account.move.send._send_mail`
# calls `message_post(attachments=[(name, raw)])` which base64-encodes
# the bytes into an ir.attachment.datas — any non-empty byte string is
# fine, but an actual PDF header helps keep downstream mimetype sniffing
# happy.
_STUB_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj<<>>endobj\n"
    b"2 0 obj<</Type/Catalog/Pages 3 0 R>>endobj\n"
    b"3 0 obj<</Type/Pages/Count 0/Kids[]>>endobj\n"
    b"trailer<</Root 2 0 R>>\n"
    b"%%EOF\n"
)


def _cleanup_invoice(env, ref):
    moves = env["account.move"].search([("ref", "=", ref)])
    for mv in moves:
        reversals = env["account.move"].search([
            ("reversed_entry_id", "=", mv.id),
        ])
        for rev in reversals:
            if rev.state == "posted":
                rev.button_draft()
            rev.button_cancel()
            rev.unlink()
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if mv.state == "posted":
            mv.button_draft()
        mv.button_cancel()
        mv.unlink()


def setup(env):
    # --- Cleanup prior runs ---
    _cleanup_invoice(env, TARGET_REF)

    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        orphans = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("ref", "=", TARGET_REF),
        ])
        for o in orphans:
            if o.state == "posted":
                o.button_draft()
            o.button_cancel()
            o.unlink()

        # Nuke any chatter mail.messages left on the partner itself from
        # prior failed runs (harmless if empty).
        env["mail.message"].search([
            ("model", "=", "res.partner"),
            ("res_id", "=", partner.id),
        ]).unlink()

    # --- Ensure the partner exists ---
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": PARTNER_EMAIL,
            "is_company": True,
        })
    else:
        partner.write({
            "email": PARTNER_EMAIL,
            "is_company": True,
        })

    # --- Ensure the product exists ---
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "list_price": 150.0,
            "invoice_policy": "order",
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({"list_price": 150.0})

    # --- Pre-set external report layout (avoid layout configurator) ---
    company = env.company
    if not company.external_report_layout_id:
        layout = env.ref(
            "web.external_layout_standard", raise_if_not_found=False
        )
        if layout:
            company.sudo().external_report_layout_id = layout.id

    # --- Create the DRAFT customer invoice ---
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": TARGET_REF,
        "invoice_date": "2026-04-15",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": product.id,
                "quantity": 1,
                "price_unit": 150.0,
                "name": PRODUCT_NAME,
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })

    # --- Post the invoice (task starts posted) ---
    invoice.action_post()

    # --- wkhtmltopdf workaround: pre-seed stub PDF bytes ---
    # After posting (name has been set to INV/YYYY/...), write the stub
    # PDF into invoice_pdf_report_file. Binary field with attachment=True
    # auto-creates ir.attachment(res_model='account.move', res_id=inv.id,
    # res_field='invoice_pdf_report_file'). invoice_pdf_report_id computes
    # to that attachment so _generate_invoice_documents skips the wkhtml
    # render path.
    invoice.sudo().write({
        "invoice_pdf_report_file": base64.b64encode(_STUB_PDF_BYTES),
    })

    # Sanity: ensure invoice_pdf_report_id is now truthy so the
    # downstream send path has something to attach.
    invoice.invalidate_recordset(fnames=['invoice_pdf_report_id'])
    # If env/cache is lazy, _compute_linked_attachment_id will populate
    # on next read inside the agent's session.
