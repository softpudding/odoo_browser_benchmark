"""Seed three draft quotations for the cancel-with-log-reason task.

Category 2 (MEDIUM): The agent must identify the correct target among
two distractors, post an internal log note with a specific reason, and
then cancel the target quotation.
"""


def setup(env):
    partner = env["res.partner"].search(
        [("name", "=", "Azure Interior")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Azure Interior",
            "email": "contact@azureinterior.com",
        })

    # Cleanup prior runs for the references used here
    refs = ["BENCH-CANCEL-01", "BENCH-NOCANCEL-A", "BENCH-NOCANCEL-B"]
    old = env["sale.order"].search([("client_order_ref", "in", refs)])
    for so in old:
        env["mail.message"].search([
            ("res_model", "=", "sale.order"),
            ("res_id", "=", so.id),
            ("subtype_id.name", "=", "Note"),
        ]).unlink()
        if so.state in ("sale",):
            so.action_cancel()
        so.unlink()

    # Ensure product exists
    product = env["product.product"].search(
        [("name", "=", "Desk Organizer")], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": "Desk Organizer",
            "type": "consu",
            "list_price": 25.0,
        })
        product = tmpl.product_variant_id

    admin = env.ref("base.user_admin")
    for ref, qty in [
        ("BENCH-CANCEL-01", 4),
        ("BENCH-NOCANCEL-A", 2),
        ("BENCH-NOCANCEL-B", 6),
    ]:
        so = env["sale.order"].create({
            "partner_id": partner.id,
            "user_id": admin.id,
            "client_order_ref": ref,
        })
        env["sale.order.line"].create({
            "order_id": so.id,
            "product_id": product.id,
            "product_uom_qty": qty,
            "price_unit": 25.0,
            "tax_ids": [(5, 0, 0)],
        })
