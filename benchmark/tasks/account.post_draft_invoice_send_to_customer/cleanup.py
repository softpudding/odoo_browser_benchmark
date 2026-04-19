"""Cleanup for account.post_draft_invoice_send_to_customer."""

TARGET_REF = "BENCH-POST-SEND-001"
PARTNER_NAME = "Bench Post Co"
PRODUCT_NAME = "Bench Posting Service"


def cleanup(env):
    moves = env["account.move"].search([("ref", "=", TARGET_REF)])
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

    partner = env["res.partner"].search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        extra_moves = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("ref", "=", TARGET_REF),
        ])
        for mv in extra_moves:
            if mv.state == "posted":
                mv.button_draft()
            mv.button_cancel()
            mv.unlink()
        partner.unlink()

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if product:
        tmpl = product.product_tmpl_id
        product.unlink()
        if tmpl and not tmpl.product_variant_ids:
            tmpl.unlink()
