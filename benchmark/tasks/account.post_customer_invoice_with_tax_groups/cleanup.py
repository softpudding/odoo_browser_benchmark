"""Cleanup for account.post_customer_invoice_with_tax_groups."""

CUSTOMER_NAME = "Bench Tax Cust"
PRODUCT_NAME = "Bench Tax Service"
TAX_10_NAME = "Bench Sale Tax 10%"
TAX_20_NAME = "Bench Sale Tax 20%"


def cleanup(env):
    customer = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", CUSTOMER_NAME)], limit=1
    )

    # Drop invoices for this customer (any state).
    if customer:
        moves = env["account.move"].with_context(active_test=False).search([
            ("partner_id", "=", customer.id),
            ("move_type", "in", ["out_invoice", "out_refund"]),
        ])
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

    prod = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if prod:
        try:
            tmpl = prod.product_tmpl_id
            prod.sudo().unlink()
            if tmpl and not tmpl.product_variant_ids:
                tmpl.sudo().unlink()
        except Exception:
            pass

    taxes = env["account.tax"].with_context(active_test=False).search([
        ("name", "in", [TAX_10_NAME, TAX_20_NAME]),
    ])
    for t in taxes:
        try:
            t.sudo().unlink()
        except Exception:
            pass

    if customer:
        try:
            customer.sudo().unlink()
        except Exception:
            pass
