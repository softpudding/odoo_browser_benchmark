"""Seed a draft quotation for the set-payment-terms-confirm task.

Category 2 (MEDIUM): Find a quotation, set payment terms, edit a line
quantity, set customer reference, and confirm. Requires multiple form
edits plus the confirm action.
"""


def setup(env):
    # --- Cleanup prior runs ---
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Azure Interior",
            "email": "azure@example.com",
        })

    # Remove any old orders for this partner with our reference
    old_orders = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "in", ["BENCH-PMT-01", "AZ-2026-Q2"]),
    ])
    for order in old_orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state == "cancel":
            order.unlink()
        elif order.state == "draft":
            order.unlink()

    # --- Ensure products exist ---
    products = {}
    for name, price in [("Desk Organizer", 25.0), ("Monitor Stand", 85.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            p = tmpl.product_variant_id
        products[name] = p

    # --- Ensure payment term exists ---
    pay_term = env["account.payment.term"].search(
        [("name", "=", "30 Net Days")], limit=1
    )
    if not pay_term:
        pay_term = env["account.payment.term"].create({
            "name": "30 Net Days",
            "line_ids": [(0, 0, {
                "value": "percent",
                "value_amount": 100,
                "nb_days": 30,
            })],
        })

    # --- Create the draft quotation ---
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "name": "BENCH-SO-PMT",
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": "BENCH-PMT-01",
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Desk Organizer"].id,
        "product_uom_qty": 5,
        "price_unit": 25.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Monitor Stand"].id,
        "product_uom_qty": 2,
        "price_unit": 85.0,
        "tax_ids": [(5, 0, 0)],
    })
