"""Seed two posted invoices for the credit note wizard task.

Category 3: Side-effect trap (wizard).
The agent must use the Credit Note (reversal) wizard on the correct
invoice, fill in the reason, and post the resulting credit note.
The distractor invoice has a confusingly similar customer name.
"""


def setup(env):
    customers = {}
    for name, email in [
        ("Lakeview Partners", "billing@lakeview-partners.example.com"),
        ("Lakeview Projects", "billing@lakeview-projects.example.com"),
    ]:
        p = env["res.partner"].search([("name", "=", name)], limit=1)
        if not p:
            p = env["res.partner"].create({"name": name, "email": email})
        customers[name] = p

    product = env["product.product"].search([("name", "=", "Professional Services")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Professional Services",
            "type": "service",
            "list_price": 100.0,
        })
        product = tmpl.product_variant_id

    # Cleanup prior runs
    for ref in ["CN-TARGET-01", "CN-IGNORE-01"]:
        old_moves = env["account.move"].search([("ref", "=", ref)])
        for mv in old_moves:
            # Also find and clean any reversals
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", mv.id),
            ])
            for rev in reversals:
                if rev.state == "posted":
                    rev.button_draft()
                rev.button_cancel()
                rev.unlink()
            # Unreconcile
            for line in mv.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if mv.state == "posted":
                mv.button_draft()
            mv.button_cancel()
            mv.unlink()

    # Create two posted invoices
    invoice_specs = [
        ("Lakeview Partners", "CN-TARGET-01", 1800.0, 18),
        ("Lakeview Projects", "CN-IGNORE-01", 2400.0, 24),
    ]

    for customer_name, ref, total, qty in invoice_specs:
        price = total / qty
        inv = env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": customers[customer_name].id,
            "ref": ref,
            "invoice_date": "2026-04-10",
            "invoice_line_ids": [
                (0, 0, {
                    "product_id": product.id,
                    "quantity": qty,
                    "price_unit": price,
                    "name": f"Professional Services for {customer_name}",
                    "tax_ids": [(5, 0, 0)],
                }),
            ],
        })
        inv.action_post()
