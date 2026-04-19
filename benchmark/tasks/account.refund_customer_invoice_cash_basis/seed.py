"""Seed a posted single-line customer invoice for the cash-basis partial refund task.

Category 3: Side-effect trap (wizard).
The agent must open the Credit Note (Reverse) wizard on a posted
single-line customer invoice (total 500.00), accept the wizard defaults
(reason + today's date + default journal), click the primary "Reverse"
button (NOT "Reverse and Create Invoice"), then on the generated draft
out_refund OVERRIDE the lone copied line's price_unit from 500.00 to
200.00 before posting the credit note via the header "Confirm" button.

The trap is single-line specific: unlike multi-line partial-refund tasks
there is no line to delete. The agent must realise that the default
reversal draft is a full 500.00 refund and edit price_unit in-place,
which most agents skip in favour of accepting the full-amount draft.
"""


TARGET_REF = "BENCH-REFUND-001"
PARTNER_NAME = "Bench Ref Co"
PRODUCT_NAME = "Bench Refund Service"


def setup(env):
    # Partner
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "ar@benchrefund.example.com",
        })

    # Product
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        template = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "service",
            "list_price": 500.0,
            "invoice_policy": "order",
        })
        product = template.product_variant_id
    else:
        product.product_tmpl_id.write({
            "list_price": 500.0,
            "type": "service",
            "invoice_policy": "order",
        })

    # Cleanup prior runs: remove any reversals linked to BENCH-REFUND-001
    # and the source invoice itself.
    old_moves = env["account.move"].search([("ref", "=", TARGET_REF)])
    for mv in old_moves:
        reversals = env["account.move"].search([
            ("reversed_entry_id", "=", mv.id),
        ])
        for rev in reversals:
            for line in rev.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
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

    # Also sweep orphan out_refund drafts/posted for this partner that a
    # prior failed oracle/agent run may have left behind.
    orphan_refunds = env["account.move"].search([
        ("move_type", "=", "out_refund"),
        ("partner_id", "=", partner.id),
    ])
    for ref in orphan_refunds:
        for line in ref.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if ref.state == "posted":
            ref.button_draft()
        ref.button_cancel()
        ref.unlink()

    # Create and post the TARGET single-line invoice (500.00 total).
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
                "name": PRODUCT_NAME,
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    invoice.action_post()
