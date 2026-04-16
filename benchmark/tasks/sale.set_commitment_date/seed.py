"""Seed a confirmed sales order for the set_commitment_date task.

Category 2 (MEDIUM): Cancel a confirmed order, reset to draft, navigate to the
Other Information tab to set the Delivery Date, and re-confirm.

The agent must use the cancel → reset → tab navigate → date edit → confirm
workflow. This tests tab navigation on the SO form plus the cancel/reconfirm
pattern, which is distinct from simple field edits.
"""

PARTNER_NAME = "Highfield Consulting"
TARGET_REF = "BENCH-COMMIT-01"
DISTRACTOR_REF = "BENCH-COMMIT-02"


def _cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", [TARGET_REF, DISTRACTOR_REF])
    ])
    for order in orders:
        for inv in order.invoice_ids:
            if inv.state == "posted":
                inv.button_draft()
            inv.unlink()
        if order.state == "sale":
            order.action_cancel()
        if order.state == "cancel":
            order.action_draft()
        order.unlink()


def _ensure_partner(env, name):
    partner = env["res.partner"].search([("name", "=", name)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": name,
            "customer_rank": 1,
        })
    return partner


def _ensure_service_product(env, name, price):
    tmpl = env["product.template"].search([("name", "=", name)], limit=1)
    if not tmpl:
        tmpl = env["product.template"].create({
            "name": name,
            "type": "service",
            "invoice_policy": "order",
            "list_price": price,
        })
    else:
        tmpl.write({"invoice_policy": "order", "list_price": price})
    return tmpl.product_variant_id


def _make_order(env, partner, product, ref):
    order = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": ref,
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": product.id,
        "product_uom_qty": 5,
        "price_unit": 800.0,
        "tax_ids": [(5, 0, 0)],
    })
    order.action_confirm()
    return order


def setup(env):
    _cleanup(env)

    partner = _ensure_partner(env, PARTNER_NAME)
    product = _ensure_service_product(env, "Platform Deployment Service", 800.0)

    _make_order(env, partner, product, TARGET_REF)
    _make_order(env, partner, product, DISTRACTOR_REF)
