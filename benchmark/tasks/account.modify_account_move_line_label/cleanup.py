"""Cleanup for account.modify_account_move_line_label."""

TARGET_REF = "BENCH-EDIT-001"
PARTNER_NAME = "Bench Edit Co"
PRODUCT_NAME = "Bench Edit Service"


def cleanup(env):
    moves = env["account.move"].search([("ref", "=", TARGET_REF)])
    for mv in moves:
        reversals = env["account.move"].search([
            ("reversed_entry_id", "=", mv.id),
        ])
        for rev in reversals:
            if rev.state == "posted":
                try:
                    rev.button_draft()
                except Exception:
                    pass
            try:
                rev.button_cancel()
            except Exception:
                pass
            try:
                rev.unlink()
            except Exception:
                pass
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            try:
                line.remove_move_reconcile()
            except Exception:
                pass
        if mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        try:
            mv.button_cancel()
        except Exception:
            pass
        try:
            mv.unlink()
        except Exception:
            pass

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
                try:
                    mv.button_draft()
                except Exception:
                    pass
            try:
                mv.button_cancel()
            except Exception:
                pass
            try:
                mv.unlink()
            except Exception:
                pass
        try:
            partner.unlink()
        except Exception:
            pass

    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if product:
        tmpl = product.product_tmpl_id
        try:
            product.unlink()
        except Exception:
            pass
        if tmpl and not tmpl.product_variant_ids:
            try:
                tmpl.unlink()
            except Exception:
                pass
