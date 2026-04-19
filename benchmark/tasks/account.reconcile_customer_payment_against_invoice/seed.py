"""Seed a posted, unpaid customer invoice for the payment-reconcile task.

Category 2: Policy trap (wizard).
The agent must open the Register Payment wizard on a posted, not-paid
customer invoice and complete it with the default amount (500.00) and the
Bank / Manual payment method, then click the primary "Create Payment"
button so the account.payment is posted and reconciled against the
invoice.
"""


TARGET_REF = "INV/BENCH/RECON"
PARTNER_NAME = "Bench Recon Co"


def setup(env):
    # Partner
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "ar@benchrecon.example.com",
        })

    # Product
    product = env["product.product"].search(
        [("name", "=", "Bench Recon Service")], limit=1
    )
    if not product:
        template = env["product.template"].create({
            "name": "Bench Recon Service",
            "type": "service",
            "list_price": 500.0,
        })
        product = template.product_variant_id
    else:
        product.product_tmpl_id.write({"list_price": 500.0})

    # Cleanup prior runs — unreconcile/cancel any related payments, reversals,
    # and the source invoice itself.
    old_moves = env["account.move"].search([("ref", "=", TARGET_REF)])
    for mv in old_moves:
        # Unreconcile linked payment matching lines before deleting
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        # Delete reversals (credit notes)
        reversals = env["account.move"].search([("reversed_entry_id", "=", mv.id)])
        for rev in reversals:
            if rev.state == "posted":
                rev.button_draft()
            rev.button_cancel()
            rev.unlink()
        if mv.state == "posted":
            mv.button_draft()
        mv.button_cancel()
        mv.unlink()

    # Sweep account.payment records for this partner (from prior runs)
    if partner:
        old_payments = env["account.payment"].search([
            ("partner_id", "=", partner.id),
        ])
        for pay in old_payments:
            if pay.state == "posted":
                # Unreconcile linked lines so the move can be cancelled
                move = pay.move_id
                if move:
                    for line in move.line_ids.filtered(
                        lambda l: l.matched_debit_ids or l.matched_credit_ids
                    ):
                        line.remove_move_reconcile()
                    pay.action_draft()
            pay.action_cancel() if hasattr(pay, "action_cancel") else None
            # Delete the underlying move if still there
            if pay.move_id and pay.move_id.state != "cancel":
                try:
                    pay.move_id.button_cancel()
                except Exception:
                    pass
            pay.unlink()

        # Sweep any orphan customer invoices/refunds for this partner
        orphans = env["account.move"].search([
            ("partner_id", "=", partner.id),
            ("move_type", "in", ["out_invoice", "out_refund"]),
        ])
        for m in orphans:
            for line in m.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if m.state == "posted":
                m.button_draft()
            m.button_cancel()
            m.unlink()

    # Create and post the target invoice
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": TARGET_REF,
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": product.id,
                "quantity": 1,
                "price_unit": 500.0,
                "name": "Bench Recon Service",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    invoice.action_post()
