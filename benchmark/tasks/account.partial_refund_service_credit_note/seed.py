"""Seed two posted invoices for a partial service refund task.

Category 3: Side-effect trap (wizard).
The agent must reverse the correct invoice, then remove the
non-refunded line so the credit note stays surgical.
"""


TARGET_REF = "CN-SERVICE-01"
DISTRACTOR_REF = "CN-SERVICE-02"


def setup(env):
    customers = {}
    for name, email in [
        ("Greenfield Manufacturing", "billing@greenfield-mfg.example.com"),
        ("Greenfield Materials", "billing@greenfield-materials.example.com"),
    ]:
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        if not partner:
            partner = env["res.partner"].create({"name": name, "email": email})
        customers[name] = partner

    products = {}
    for name, price in [("Warehouse Audit", 475.0), ("Onsite Training", 600.0)]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "service",
                "list_price": price,
            })
            product = template.product_variant_id
        products[name] = product

    for ref in [TARGET_REF, DISTRACTOR_REF]:
        moves = env["account.move"].search([("ref", "=", ref)])
        for move in moves:
            reversals = env["account.move"].search([("reversed_entry_id", "=", move.id)])
            for reversal in reversals:
                if reversal.state == "posted":
                    reversal.button_draft()
                reversal.button_cancel()
                reversal.unlink()
            for line in move.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if move.state == "posted":
                move.button_draft()
            move.button_cancel()
            move.unlink()

    target = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": customers["Greenfield Manufacturing"].id,
        "ref": TARGET_REF,
        "invoice_date": "2026-04-18",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Warehouse Audit"].id,
                "quantity": 2,
                "price_unit": 475.0,
                "name": "Warehouse Audit",
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": products["Onsite Training"].id,
                "quantity": 1,
                "price_unit": 600.0,
                "name": "Onsite Training",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    target.action_post()

    distractor = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": customers["Greenfield Materials"].id,
        "ref": DISTRACTOR_REF,
        "invoice_date": "2026-04-19",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Warehouse Audit"].id,
                "quantity": 1,
                "price_unit": 475.0,
                "name": "Warehouse Audit",
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": products["Onsite Training"].id,
                "quantity": 2,
                "price_unit": 600.0,
                "name": "Onsite Training",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    distractor.action_post()
