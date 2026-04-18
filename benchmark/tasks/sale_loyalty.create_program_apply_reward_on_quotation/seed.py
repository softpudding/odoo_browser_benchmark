"""Seed for sale_loyalty.create_program_apply_reward_on_quotation."""


def setup(env):
    env["sale.order"].search([("client_order_ref", "=", "HARBOR-LOYALTY-01")]).unlink()
    env["loyalty.program"].search([("name", "=", "Harbor 15% Quotation Reward")]).unlink()
    env["product.template"].search([("name", "=", "Harbor Signal Lamp")]).unlink()

    partner = env["res.partner"].search([("name", "=", "Harbor Trading")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Harbor Trading", "customer_rank": 1})

    product = env["product.product"].create({
        "name": "Harbor Signal Lamp",
        "type": "consu",
        "list_price": 120.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })

    order = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "HARBOR-LOYALTY-01",
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": product.id,
        "product_uom_qty": 1.0,
        "price_unit": 120.0,
        "tax_ids": [(5, 0, 0)],
    })
