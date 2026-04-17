"""Seed a draft quotation for sale.update_quote_payment_terms_validity_confirm."""


def setup(env):
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Azure Interior", "email": "azure@example.com"})
    old_orders = env["sale.order"].search([("partner_id", "=", partner.id), ("client_order_ref", "=", "BENCH-PMT-02")])
    for order in old_orders:
        if order.state == "sale":
            order.action_cancel()
        order.unlink()
    products = {}
    for name, price in [("Desk Organizer", 25.0), ("Monitor Stand", 85.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({"name": name, "type": "consu", "list_price": price})
            p = tmpl.product_variant_id
        products[name] = p
    pay_term = env["account.payment.term"].search([("name", "=", "30 Net Days")], limit=1)
    if not pay_term:
        env["account.payment.term"].create({
            "name": "30 Net Days",
            "line_ids": [(0, 0, {"value": "percent", "value_amount": 100, "nb_days": 30})],
        })
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "name": "BENCH-SO-PMT-02",
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": "BENCH-PMT-02",
    })
    env["sale.order.line"].create({"order_id": so.id, "product_id": products["Desk Organizer"].id, "product_uom_qty": 5, "price_unit": 25.0, "tax_ids": [(5,0,0)]})
    env["sale.order.line"].create({"order_id": so.id, "product_id": products["Monitor Stand"].id, "product_uom_qty": 2, "price_unit": 85.0, "tax_ids": [(5,0,0)]})
