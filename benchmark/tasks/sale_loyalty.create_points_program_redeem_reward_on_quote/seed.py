"""Seed for sale_loyalty.create_points_program_redeem_reward_on_quote."""

def setup(env):
    env["sale.order"].search([("client_order_ref", "=", "ROTOR-PTS-01")]).unlink()
    env["loyalty.program"].search([("name", "=", "Rotor Points Reward")]).unlink()
    env["product.template"].search([("name", "=", "Rotor Service Kit")]).unlink()
    partner = env["res.partner"].search([("name", "=", "Rotor Trading")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Rotor Trading", "customer_rank": 1})
    prod = env["product.product"].create({
        "name": "Rotor Service Kit",
        "type": "consu",
        "list_price": 150.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    order = env["sale.order"].create({"partner_id": partner.id, "client_order_ref": "ROTOR-PTS-01"})
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": prod.id,
        "product_uom_qty": 1,
        "price_unit": 150.0,
        "tax_ids": [(5, 0, 0)],
    })
