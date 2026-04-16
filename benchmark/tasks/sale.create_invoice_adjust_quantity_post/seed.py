"""Seed a confirmed sales order for the create-invoice-adjust-quantity-post task.

Category 2 (MEDIUM): Create an invoice from an existing sales order, adjust
invoice fields on the generated draft, then confirm it.
"""

PARTNER_NAME = "Northwind Studio"
TARGET_REF = "MED-INV-SO-01"
DISTRACTOR_REF = "MED-INV-SO-02"


def _cleanup_orders(env, refs):
    orders = env["sale.order"].search([("client_order_ref", "in", refs)])
    for order in orders:
        for invoice in order.invoice_ids.filtered(
            lambda move: move.move_type == "out_invoice"
        ):
            if invoice.state == "posted":
                invoice.button_draft()
            invoice.unlink()
        if order.state == "sale":
            order.action_cancel()
        order.unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "invoice_policy": "order",
            "list_price": price,
            "standard_price": price,
        })
        return product

    tmpl = env["product.template"].create({
        "name": name,
        "type": "service",
        "invoice_policy": "order",
        "list_price": price,
        "standard_price": price,
    })
    return tmpl.product_variant_id


def _make_order(env, partner, ref, support, implementation):
    admin = env.ref("base.user_admin")
    order = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": ref,
    })

    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": support.id,
        "product_uom_qty": 3,
        "price_unit": 1500.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": implementation.id,
        "product_uom_qty": 1,
        "price_unit": 2400.0,
        "tax_ids": [(5, 0, 0)],
    })
    order.action_confirm()
    return order


def setup(env):
    _cleanup_orders(env, [TARGET_REF, DISTRACTOR_REF])

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "billing@northwind-studio.example.com",
        })

    support = _ensure_product(env, "Support Retainer", 1500.0)
    implementation = _ensure_product(env, "Implementation Block", 2400.0)
    payment_term = env["account.payment.term"].search(
        [("name", "=", "30 Net Days")], limit=1
    )
    if not payment_term:
        env["account.payment.term"].create({
            "name": "30 Net Days",
            "line_ids": [(0, 0, {
                "value": "percent",
                "value_amount": 100,
                "nb_days": 30,
            })],
        })

    _make_order(env, partner, TARGET_REF, support, implementation)
    _make_order(env, partner, DISTRACTOR_REF, support, implementation)
