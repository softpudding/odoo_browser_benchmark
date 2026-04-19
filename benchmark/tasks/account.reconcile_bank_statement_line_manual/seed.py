"""Seed for account.reconcile_bank_statement_line_manual.

Category 1: Closed-loop cross-module (hard).

Seeds:
  1. A partner "Bench Reconcile Customer".
  2. A posted customer invoice for €500 (move_type='out_invoice',
     state='posted', payment_state='not_paid').
  3. An unreconciled bank statement line in the Bank journal for the same
     customer with amount 500 and payment_ref 'Bench Reconcile 500'.

The agent must open the bank reconciliation widget and manually match the
bank statement line against the open customer invoice so that the invoice
becomes fully paid.
"""

PARTNER_NAME = "Bench Reconcile Customer"
PAYMENT_REF = "Bench Reconcile 500"
PRODUCT_NAME = "Bench Reconcile Service"
INVOICE_REF = "BENCH-RECO-01"
INVOICE_AMOUNT = 500.00


def _cleanup(env):
    # Unreconcile + unlink any prior bank statement lines we seeded.
    stl_model = env["account.bank.statement.line"]
    old_stls = stl_model.search([("payment_ref", "=", PAYMENT_REF)])
    for stl in old_stls:
        try:
            stl.action_undo_reconciliation()
        except Exception:
            pass
        mv = stl.move_id
        # Detach from any statement to allow unlink.
        try:
            if stl.statement_id:
                stl.statement_id = False
        except Exception:
            pass
        if mv and mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        try:
            stl.unlink()
        except Exception:
            pass
        if mv and mv.exists():
            try:
                if mv.state != "cancel":
                    mv.button_cancel()
            except Exception:
                pass
            try:
                mv.unlink()
            except Exception:
                pass

    # Remove any prior invoices for this partner.
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        old_invs = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "=", "out_invoice"),
        ])
        for inv in old_invs:
            # Unreconcile any partial reconciliations on the invoice lines
            for line in inv.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                try:
                    line.remove_move_reconcile()
                except Exception:
                    pass
            # Also clean up related reversals/payments
            if inv.state == "posted":
                try:
                    inv.button_draft()
                except Exception:
                    pass
            try:
                inv.button_cancel()
            except Exception:
                pass
            try:
                inv.unlink()
            except Exception:
                pass


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        return partner
    return env["res.partner"].create({
        "name": PARTNER_NAME,
        "company_type": "person",
        "email": "bench.reconcile@example.com",
    })


def _ensure_product(env):
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if product:
        return product
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "service",
        "list_price": INVOICE_AMOUNT,
        "invoice_policy": "order",
    })
    return tmpl.product_variant_id


def _ensure_bank_journal(env):
    """Return a bank journal. Ensures its default account exists."""
    bank = env["account.journal"].search([("type", "=", "bank")], limit=1)
    if not bank:
        bank = env["account.journal"].create({
            "name": "Bank",
            "type": "bank",
            "code": "BNK1",
        })
    return bank


def setup(env):
    _cleanup(env)

    partner = _ensure_partner(env)
    product = _ensure_product(env)
    bank_journal = _ensure_bank_journal(env)

    # Create posted customer invoice for 500.
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": INVOICE_REF,
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": product.id,
                "quantity": 1,
                "price_unit": INVOICE_AMOUNT,
                "name": "Bench Reconcile consulting service",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    invoice.action_post()

    # Create unreconciled bank statement line for 500.
    env["account.bank.statement.line"].create({
        "journal_id": bank_journal.id,
        "date": "2026-04-15",
        "payment_ref": PAYMENT_REF,
        "partner_id": partner.id,
        "amount": INVOICE_AMOUNT,
    })

    # Ensure admin has accounting groups so the reconcile UI renders.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "account.group_account_readonly",
        "account.group_account_invoice",
        "account.group_account_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})
