"""Postcondition checks for account.print_invoice_pdf_attach_to_partner.

Validates:
  1. Target invoice BENCH-PRINT-001 is still posted (unchanged from seed),
     partner Bench Print Co, amount_total == 150.0.
  2. At least one NEW mail.message was posted on the invoice's chatter
     AFTER the seed (message_type in comment/email/email_outgoing, subtype
     mail.mt_comment), i.e. from the agent's Send & Print action.
  3. That new mail.message carries at least one ir.attachment whose
     filename ends with '.pdf' OR whose mimetype is 'application/pdf'
     (this is the PDF generated and attached by the send wizard via
     `_send_mail(... attachments=[(pdf_name, pdf_raw)])`).

Note (pre-seeded stub PDF): the seed writes a stub into
`invoice_pdf_report_file` so wkhtmltopdf is bypassed, but that stub is
on the *binary-field* ir.attachment (res_field='invoice_pdf_report_file'),
NOT on any mail.message. Passing the check therefore requires the agent
to actually trigger the Send flow so that `_send_mails` posts a new
mail.message whose attachment_ids include the PDF. Clicking Discard,
unchecking Email, or leaving Print unchecked (the latter does NOT in
fact prevent the PDF from being attached via _get_invoice_extra_attachments,
but checking it signals to the wizard that print-method is active and
keeps the wizard on the send path) all end without a posted mail.message,
which fails check (2).
"""

TARGET_REF = "BENCH-PRINT-001"
PARTNER_NAME = "Bench Print Co"


def _attachment_is_pdf(att):
    name = (att.name or "").strip().lower()
    mimetype = (att.mimetype or "").strip().lower()
    return name.endswith(".pdf") or mimetype == "application/pdf"


def check(env):
    failures = []

    inv = env["account.move"].search(
        [("ref", "=", TARGET_REF)], limit=1
    )
    if not inv:
        return [f"Target invoice {TARGET_REF!r} not found"]

    # (1) Invoice integrity: still posted, partner & total unchanged.
    if inv.move_type != "out_invoice":
        failures.append(
            f"Invoice move_type is {inv.move_type!r}, expected 'out_invoice'"
        )
    if inv.state != "posted":
        failures.append(
            f"Invoice state is {inv.state!r}, expected 'posted' (did "
            f"you reset to draft / cancel?)"
        )
        return failures
    if inv.partner_id.name != PARTNER_NAME:
        failures.append(
            f"Invoice partner is {inv.partner_id.name!r}, expected "
            f"{PARTNER_NAME!r}"
        )
    if abs(inv.amount_total - 150.0) > 0.01:
        failures.append(
            f"Invoice amount_total is {inv.amount_total}, expected 150.0 "
            f"(do not edit the lines)"
        )

    # (2) A mail.message must exist on the invoice from the Send wizard.
    mt_comment = env.ref("mail.mt_comment", raise_if_not_found=False)
    messages = env["mail.message"].search([
        ("model", "=", "account.move"),
        ("res_id", "=", inv.id),
    ], order="id desc")

    if not messages:
        return failures + [
            "No mail.message posted on the invoice — expected at least one "
            "chatter message from the Send & Print wizard. Did you click "
            "Discard instead of Send?"
        ]

    # Accept the Send wizard's standard subtype (mail.mt_comment) AND
    # message_type in ('email', 'comment', 'email_outgoing').
    send_candidates = messages
    if mt_comment:
        send_candidates = messages.filtered(
            lambda m: (
                m.subtype_id.id == mt_comment.id
                and m.message_type in ("email", "comment", "email_outgoing")
            )
        )

    if not send_candidates:
        subtypes = messages.mapped("subtype_id.name")
        types = messages.mapped("message_type")
        return failures + [
            "No outbound Send-wizard mail.message found on the invoice. "
            f"Messages present (subtype/message_type): "
            f"{list(zip(subtypes, types))}. Expected a mail.message with "
            f"subtype 'mail.mt_comment' AND message_type in "
            f"('email','comment','email_outgoing'). Did the agent click "
            f"Discard, or uncheck Email before Send?"
        ]

    # (3) At least one PDF attachment on one of the Send-wizard messages.
    msgs_with_pdf = []
    for msg in send_candidates:
        if any(_attachment_is_pdf(att) for att in msg.attachment_ids):
            msgs_with_pdf.append(msg)

    if not msgs_with_pdf:
        # Diagnostic: dump attachment names/mimetypes on the wizard
        # messages so calibration failures are easy to read.
        diag = []
        for m in send_candidates:
            diag.append({
                "id": m.id,
                "attachments": [
                    (a.name, a.mimetype) for a in m.attachment_ids
                ],
            })
        failures.append(
            "The Send-wizard mail.message(s) exist, but none carry a PDF "
            "attachment (filename ending .pdf or mimetype "
            "'application/pdf'). Did you forget to tick the 'by Print' "
            f"sending-method checkbox in the wizard? Message attachments "
            f"seen: {diag}"
        )

    return failures
