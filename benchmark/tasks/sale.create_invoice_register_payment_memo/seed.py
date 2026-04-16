"""Seed a medium sales-to-invoice-to-payment workflow.

Category 1 (MEDIUM): the agent must create an invoice from the right sales
order, post it, and complete the payment wizard with exact non-default values.
"""

PARTNER_NAME = "Brightwave Labs"
TARGET_REF = "PAYFLOW-01"
DISTRACTOR_REF = "PAYFLOW-02"


def _cleanup_orders(env, refs):
    orders = env["sale.order"].search([("client_order_ref", "in", refs)])
    for order in orders:
        for invoice in order.invoice_ids.filtered(
            lambda move: move.move_type == "out_invoice"
        ):
            for payment in invoice._get_reconciled_payments():
                if payment.state == "posted":
                    payment.action_draft()
                payment.unlink()
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


def _make_order(env, partner, ref, support, workshop):
    admin = env.ref("base.user_admin")
    order = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": ref,
    })

    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": support.id,
        "product_uom_qty": 2,
        "price_unit": 1200.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": workshop.id,
        "product_uom_qty": 1,
        "price_unit": 1800.0,
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
            "email": "billing@brightwave.example.com",
            "customer_rank": 1,
        })

    support = _ensure_product(env, "Support Subscription", 1200.0)
    workshop = _ensure_product(env, "Launch Workshop", 1800.0)

    _make_order(env, partner, TARGET_REF, support, workshop)
    _make_order(env, partner, DISTRACTOR_REF, support, workshop)
