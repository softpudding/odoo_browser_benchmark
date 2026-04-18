"""Seed for delivery.country_rule_and_free_threshold_apply_to_so."""


TARGET_REF = "SHIP-US-100"
DISTRACTOR_REF = "SHIP-CA-100"


def setup(env):
    env["sale.order"].search([
        ("client_order_ref", "in", [TARGET_REF, DISTRACTOR_REF]),
    ]).unlink()
    env["delivery.carrier"].search([
        ("name", "=", "US Harbor Freight"),
    ]).unlink()
    env["product.template"].search([
        ("name", "in", ["Bench Freight Item", "US Harbor Shipping"]),
    ]).unlink()
    env["res.partner"].search([
        ("name", "in", ["Bench US Customer", "Bench CA Customer"]),
    ]).unlink()

    us = env["res.country"].search([("code", "=", "US")], limit=1)
    ca = env["res.country"].search([("code", "=", "CA")], limit=1)
    if not us or not ca:
        raise RuntimeError("US and CA countries must exist")

    us_partner = env["res.partner"].create({
        "name": "Bench US Customer",
        "country_id": us.id,
    })
    ca_partner = env["res.partner"].create({
        "name": "Bench CA Customer",
        "country_id": ca.id,
    })

    product = env["product.template"].create({
        "name": "Bench Freight Item",
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 60.0,
    })

    order_line = [(0, 0, {
        "product_id": product.product_variant_id.id,
        "name": "Bench Freight Item",
        "product_uom_qty": 2,
        "price_unit": 60.0,
    })]

    env["sale.order"].create({
        "partner_id": us_partner.id,
        "partner_shipping_id": us_partner.id,
        "client_order_ref": TARGET_REF,
        "order_line": order_line,
    })
    env["sale.order"].create({
        "partner_id": ca_partner.id,
        "partner_shipping_id": ca_partner.id,
        "client_order_ref": DISTRACTOR_REF,
        "order_line": order_line,
    })
