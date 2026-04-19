"""Postcondition checks for account.post_draft_invoice_send_to_customer.

Validates:
  1. Invoice BENCH-POST-SEND-001 is in state 'posted' (move_type='out_invoice'),
     with amounts unchanged.
  2. At least one mail.message was posted on the invoice as the result
     of the send wizard — i.e., a chatter message with subtype
     'mail.mt_comment' (the account.move.send._send_mail path posts
     message_type='comment' with the template subject/body), and with
     the invoice partner in partner_ids OR an associated
     mail.notification row. This proves the agent clicked the primary
     Send button in the wizard (NOT Discard, and did not uncheck
     Email).

Note: the benchmark environment does not have wkhtmltopdf installed,
which means the invoice's `is_move_sent` flag does NOT flip to True
even after a successful send (PDF generation is a separate code path).
The seed pre-fills `invoice_pdf_report_file` so the wizard skips
wkhtmltopdf and completes the mail-post path, but the
`_link_invoice_documents` step that sets `is_move_sent` requires a
freshly-generated pdf_attachment_values payload it never receives. We
gate on the mail.message post instead.
"""

TARGET_REF = "BENCH-POST-SEND-001"
PARTNER_NAME = "Bench Post Co"


def check(env):
    failures = []

    inv = env["account.move"].search(
        [("ref", "=", TARGET_REF)], limit=1
    )
    if not inv:
        return [f"Target invoice {TARGET_REF!r} not found"]

    if inv.move_type != "out_invoice":
        failures.append(
            f"Invoice move_type is {inv.move_type!r}, expected 'out_invoice'"
        )

    if inv.state != "posted":
        failures.append(
            f"Invoice state is {inv.state!r}, expected 'posted' "
            f"(did you click Confirm in the header?)"
        )
        return failures

    if inv.partner_id.name != PARTNER_NAME:
        failures.append(
            f"Invoice partner is {inv.partner_id.name!r}, "
            f"expected {PARTNER_NAME!r}"
        )

    # Verify a mail.message from the send wizard was posted on the invoice.
    # account.move.send._send_mail posts message_type='comment' with
    # subtype mail.mt_comment (via message_post's default body+partners
    # pipeline using the template).
    messages = env["mail.message"].search([
        ("model", "=", "account.move"),
        ("res_id", "=", inv.id),
    ])
    if not messages:
        failures.append(
            "No mail.message found on the invoice — expected at least one "
            "chatter message from the Send wizard."
        )
        return failures

    mt_comment = env.ref("mail.mt_comment", raise_if_not_found=False)

    # Accept either:
    #   - a mail.message whose subtype_id is mail.mt_comment AND
    #     message_type is 'comment'/'email'/'email_outgoing', OR
    #   - any mail.notification with notification_type='email' tied to
    #     a message on this invoice.
    comment_msg = env["mail.message"]
    if mt_comment:
        comment_msg = messages.filtered(
            lambda m: m.subtype_id.id == mt_comment.id
            and m.message_type in ("email", "comment", "email_outgoing")
        )

    email_notif = env["mail.notification"].search([
        ("mail_message_id", "in", messages.ids),
        ("notification_type", "=", "email"),
    ], limit=1)

    if not comment_msg and not email_notif:
        subtypes = messages.mapped("subtype_id.name")
        types = messages.mapped("message_type")
        failures.append(
            "No outbound Send-wizard email message found on the invoice. "
            f"Messages present (subtype/message_type): {list(zip(subtypes, types))}. "
            "Expected a mail.message with subtype 'mail.mt_comment' "
            "(the template send), OR a mail.notification with "
            "notification_type='email'. Did the agent click Discard, or "
            "uncheck Email before clicking Send?"
        )

    # Amount sanity: agent must not edit the invoice lines/totals.
    if abs(inv.amount_total - 200.0) > 0.01:
        failures.append(
            f"Invoice amount_total is {inv.amount_total}, expected 200.0 — "
            "the agent should not edit the lines."
        )

    return failures
