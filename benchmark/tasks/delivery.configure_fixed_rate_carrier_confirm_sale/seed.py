"""Seed for delivery.configure_fixed_rate_carrier_confirm_sale."""


def setup(env):
    env["sale.order"].search([("client_order_ref", "=", "HARBOR-SHIP-01")]).unlink()
    env["delivery.carrier"].search([("name", "=", "Harbor Flat Freight")]).unlink()
    env["product.template"].search([
        ("name", "in", ["Harbor Crate", "Harbor Flat Freight Service"]),
    ]).unlink()

    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Azure Interior"})

    product_tmpl = env["product.template"].create({
        "name": "Harbor Crate",
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 55.0,
        "weight": 2.5,
    })

    env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "HARBOR-SHIP-01",
        "order_line": [(0, 0, {
            "product_id": product_tmpl.product_variant_id.id,
            "name": "Harbor Crate",
            "product_uom_qty": 2,
            "price_unit": 55.0,
        })],
    })
