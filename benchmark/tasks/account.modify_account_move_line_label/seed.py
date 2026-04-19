"""Seed data for account.modify_account_move_line_label.

Category: recovery_rollback (MEDIUM).

Seeds a POSTED customer invoice (out_invoice) with a single product
line whose `name` (Label) is 'Service' and total 100.00 (taxes cleared
for clean math). The agent must:
  1. Open BENCH-EDIT-001.
  2. Click 'Reset to Draft' in the header.
  3. Edit the line's Label from 'Service' to 'Corrected description'.
  4. Click 'Confirm' to repost the invoice.

Final expected state: state='posted', single line name='Corrected
description', amount_total=100.00 unchanged.
"""

TARGET_REF = "BENCH-EDIT-001"
PARTNER_NAME = "Bench Edit Co"
PARTNER_EMAIL = "ap@benchedit.example.com"
PRODUCT_NAME = "Bench Edit Service"
ORIGINAL_LABEL = "Service"


def _cleanup_invoice(env, ref):
    moves = env["account.move"].search([("ref", "=", ref)])
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
                try:
                    o.button_draft()
                except Exception:
                    pass
            try:
                o.button_cancel()
            except Exception:
                pass
            try:
                o.unlink()
            except Exception:
                pass

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
            "list_price": 100.0,
            "invoice_policy": "order",
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({"list_price": 100.0})

    # --- Create the POSTED customer invoice ---
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": TARGET_REF,
        "invoice_date": "2026-04-15",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": product.id,
                "quantity": 1,
                "price_unit": 100.0,
                "name": ORIGINAL_LABEL,
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    invoice.action_post()
