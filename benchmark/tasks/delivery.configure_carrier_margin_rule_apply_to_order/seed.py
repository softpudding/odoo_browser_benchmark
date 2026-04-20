"""Seed for delivery.configure_carrier_margin_rule_apply_to_order."""

def setup(env):
    env["sale.order"].search([("client_order_ref", "=", "MARGIN-DEL-01")]).unlink()
    env["delivery.carrier"].search([("name", "=", "Bench Margin Courier")]).unlink()
    env["product.template"].search([("name", "in", ["Bench Margin Widget", "Bench Margin Shipping"])]).unlink()
    partner = env["res.partner"].search([("name", "=", "Margin Freight Labs")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Margin Freight Labs", "customer_rank": 1})
    prod = env["product.template"].create({
        "name": "Bench Margin Widget",
        "type": "consu",
        "sale_ok": True,
        "list_price": 30.0,
        "weight": 2.0,
    }).product_variant_id
    env["product.template"].create({
        "name": "Bench Margin Shipping",
        "type": "service",
        "sale_ok": False,
        "purchase_ok": False,
        "invoice_policy": "order",
        "list_price": 0.0,
    })
    env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "MARGIN-DEL-01",
        "order_line": [(0, 0, {
            "product_id": prod.id,
            "name": "Bench Margin Widget",
            "product_uom_qty": 1,
            "price_unit": 30.0,
        })],
    })
