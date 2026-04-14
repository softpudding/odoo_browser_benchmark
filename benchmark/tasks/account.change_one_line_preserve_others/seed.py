"""Seed a posted invoice where one line needs surgical qty edit.

Category 3: Side-effect trap.
The invoice is already posted.  Agent must reset to draft, change exactly
one line's quantity, and re-post without corrupting the other three lines.
"""


def setup(env):
    partner = env["res.partner"].search([("name", "=", "Redwood Consulting")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Redwood Consulting",
            "email": "billing@redwood.example.com",
        })

    products = {}
    for name, price in [("Strategy Report", 3000.0), ("Market Analysis", 1500.0),
                        ("Risk Assessment", 2200.0), ("Compliance Audit", 800.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "service",
                "list_price": price,
            })
            p = tmpl.product_variant_id
        else:
            p.product_tmpl_id.write({"list_price": price})
        products[name] = p

    # --- Cleanup prior runs ---
    old_invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("ref", "=", "SURG-EDIT-01"),
    ])
    for inv in old_invoices:
        if inv.state == "posted":
            inv.button_draft()
        if inv.state == "draft":
            inv.button_cancel()
        inv.unlink()

    # --- Create and post the invoice ---
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": "SURG-EDIT-01",
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Strategy Report"].id,
                "quantity": 1,
                "price_unit": 3000.0,
                "discount": 0.0,
                "name": "Strategy Report",
            }),
            (0, 0, {
                "product_id": products["Market Analysis"].id,
                "quantity": 2,
                "price_unit": 1500.0,
                "discount": 10.0,
                "name": "Market Analysis",
            }),
            (0, 0, {
                "product_id": products["Risk Assessment"].id,
                "quantity": 1,
                "price_unit": 2200.0,
                "discount": 5.0,
                "name": "Risk Assessment",
            }),
            (0, 0, {
                "product_id": products["Compliance Audit"].id,
                "quantity": 3,
                "price_unit": 800.0,
                "discount": 0.0,
                "name": "Compliance Audit",
            }),
        ],
    })
    invoice.action_post()
