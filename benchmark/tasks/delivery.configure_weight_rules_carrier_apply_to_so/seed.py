"""Seed for delivery.configure_weight_rules_carrier_apply_to_so."""


def setup(env):
    # Cleanup any prior run state.
    env["sale.order"].search([("client_order_ref", "=", "S-BENCH-DEL-001")]).unlink()
    env["delivery.carrier"].search([("name", "=", "Bench Weight Courier")]).unlink()
    env["product.template"].search([
        ("name", "in", ["Bench Weighted Widget", "Bench Shipping Charge"]),
    ]).unlink()

    partner = env["res.partner"].search([("name", "=", "Bench Delivery Co")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Bench Delivery Co"})

    product_tmpl = env["product.template"].create({
        "name": "Bench Weighted Widget",
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 40.0,
        "weight": 3.0,
    })

    env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "S-BENCH-DEL-001",
        "order_line": [(0, 0, {
            "product_id": product_tmpl.product_variant_id.id,
            "name": "Bench Weighted Widget",
            "product_uom_qty": 1,
            "price_unit": 40.0,
        })],
    })
