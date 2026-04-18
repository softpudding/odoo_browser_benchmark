"""Seed a posted customer invoice for the partial reversal task.

Category 3: Side-effect trap (wizard).
The agent must open the Reverse wizard on a posted invoice, fill the
reason, pick the non-default "Reverse" button (which creates an editable
draft credit note — the other button is "Reverse and Create Invoice"),
then surgically trim the draft to a single line at a reduced quantity
before posting.
"""


TARGET_REF = "INV/BENCH/001"


def setup(env):
    # Partner
    partner = env["res.partner"].search([("name", "=", "Bench AR Co")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Bench AR Co",
            "email": "ar@bench.example.com",
        })

    # Products
    products = {}
    for name, price in [("Bench Item A", 100.0), ("Bench Item B", 50.0)]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            product = template.product_variant_id
        else:
            product.product_tmpl_id.write({"list_price": price})
        products[name] = product

    # Cleanup prior runs: remove any reversals linked to INV/BENCH/001
    # and the source invoice itself.
    old_moves = env["account.move"].search([("ref", "=", TARGET_REF)])
    for mv in old_moves:
        reversals = env["account.move"].search([("reversed_entry_id", "=", mv.id)])
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

    # Also sweep orphan out_refund drafts for this partner that a prior
    # failed oracle/agent run may have left behind.
    orphan_refunds = env["account.move"].search([
        ("move_type", "=", "out_refund"),
        ("partner_id", "=", partner.id),
        ("state", "=", "draft"),
    ])
    for ref in orphan_refunds:
        ref.button_cancel()
        ref.unlink()

    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": TARGET_REF,
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Bench Item A"].id,
                "quantity": 4,
                "price_unit": 100.0,
                "name": "Bench Item A",
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": products["Bench Item B"].id,
                "quantity": 2,
                "price_unit": 50.0,
                "name": "Bench Item B",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    invoice.action_post()
