"""Seed a posted customer invoice for the register-payment-defaults task.

Category 1: Accept-defaults wizard (EASY).
The agent must open a posted invoice, click Pay to open the Register Payment
wizard, accept all defaults, and click Create Payment. The invoice payment_state
should change from 'not_paid' to 'paid' or 'in_payment'.
"""


def setup(env):
    # --- Cleanup prior runs ---
    # Remove any payments created by previous runs
    old_payments = env["account.payment"].search([("memo", "=", "BENCH-PAY-01")])
    for pmt in old_payments:
        if pmt.state == "posted":
            pmt.action_draft()
        pmt.unlink()

    # Remove any prior invoice runs
    old_moves = env["account.move"].search([("ref", "=", "BENCH-PAY-01")])
    for mv in old_moves:
        # Unreconcile any payment lines
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if mv.state == "posted":
            mv.button_draft()
        mv.unlink()

    # --- Create partner ---
    partner = env["res.partner"].search([("name", "=", "Lakeview Partners")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Lakeview Partners",
            "email": "billing@lakeview-partners.example.com",
        })

    # --- Create product if needed ---
    product = env["product.product"].search(
        [("name", "=", "Professional Services")], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": "Professional Services",
            "type": "service",
            "list_price": 100.0,
        })
        product = tmpl.product_variant_id

    # --- Create the target invoice ---
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": "BENCH-PAY-01",
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": product.id,
                "quantity": 10,
                "price_unit": 100.0,
                "name": "Consulting services - April 2026",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })

    # --- Post the invoice ---
    invoice.action_post()
