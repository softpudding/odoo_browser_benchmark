"""Seed data for account.post_draft_invoice_send_to_customer.

Category: policy_trap (MEDIUM).

Seeds a single DRAFT customer invoice (out_invoice) for a seeded partner
with a service line totaling 200.00 (taxes cleared for clean math).
The agent must:
  1. Click Confirm to post the draft.
  2. Click Send in the header (which opens the account.move.send.wizard).
  3. Click the primary Send button in the wizard — NOT Discard, and
     NOT uncheck the Email method.

To avoid a spurious layout-configurator pre-wizard, we force the
company's `external_report_layout_id` to the 'Standard' report layout
so that clicking Send goes directly to the send wizard.
"""

TARGET_REF = "BENCH-POST-SEND-001"
PARTNER_NAME = "Bench Post Co"
PARTNER_EMAIL = "billing@benchpost.example.com"
PRODUCT_NAME = "Bench Posting Service"


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

    # Also sweep any orphaned drafts / posted for this partner with this ref.
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

    # --- Ensure the partner exists with an email ---
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
            "list_price": 200.0,
            "invoice_policy": "order",
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({"list_price": 200.0})

    # --- Pre-set the company's external report layout so clicking Send
    # does not trigger the base_document_layout configurator wizard. ---
    company = env.company
    if not company.external_report_layout_id:
        layout = env.ref(
            "web.external_layout_standard", raise_if_not_found=False
        )
        if layout:
            company.sudo().external_report_layout_id = layout.id
    # discard_logo_check sidesteps the no-logo branch but layout is
    # the proper toggle.

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
                "price_unit": 200.0,
                "name": PRODUCT_NAME,
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })

    # wkhtmltopdf workaround: the benchmark environment does NOT have
    # wkhtmltopdf installed. Without it, the account.move.send wizard's
    # PDF generation step raises and the email is never sent. We seed a
    # stub PDF attachment so that account.move._prepare_invoice_pdf_report
    # sees `invoice_pdf_report_id` already set and skips the wkhtmltopdf
    # render path. The send wizard then proceeds to _hook_if_success →
    # _send_mails, posting the outbound email mail.message on the chatter
    # that our check.py looks for.
    # This matches the pattern used elsewhere in the benchmark for
    # document-send tasks that must run without wkhtmltopdf.
    import base64
    stub_pdf = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
    invoice.sudo().write({
        "invoice_pdf_report_file": base64.b64encode(stub_pdf),
    })
    # leave in draft state (no action_post)
