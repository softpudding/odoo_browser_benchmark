"""Seed a confirmed sale order for a wrong-customer recovery task.

Category 4: Recovery and rollback.
The agent must cancel the confirmed order, then recreate it for the
correct customer with identical lines.
"""


TARGET_REF = "SALE-FIX-12"
REPLACEMENT_REF = "SALE-FIX-12-WEST"


def setup(env):
    customers = {}
    for name, email in [
        ("Harbor Retail East", "ops-east@harbor-retail.example.com"),
        ("Harbor Retail West", "ops-west@harbor-retail.example.com"),
    ]:
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        if not partner:
            partner = env["res.partner"].create({"name": name, "email": email})
        customers[name] = partner

    products = {}
    for name, price in [("Counter Display", 210.0), ("Shelf Signage Kit", 48.0)]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
            product = template.product_variant_id
        products[name] = product

    orders = env["sale.order"].search([
        ("client_order_ref", "in", [TARGET_REF, REPLACEMENT_REF]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel"):
            order.unlink()

    order = env["sale.order"].create({
        "partner_id": customers["Harbor Retail East"].id,
        "client_order_ref": TARGET_REF,
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": products["Counter Display"].id,
        "product_uom_qty": 4,
        "price_unit": 210.0,
        "name": "Counter Display",
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": products["Shelf Signage Kit"].id,
        "product_uom_qty": 7,
        "price_unit": 48.0,
        "name": "Shelf Signage Kit",
        "tax_ids": [(5, 0, 0)],
    })
    order.action_confirm()
