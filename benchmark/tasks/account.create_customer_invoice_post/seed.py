"""Seed data for account.create_customer_invoice_post."""

PARTNER_NAME = "Northwind Advisory"
INVOICE_REF = "NWA-AR-220"
LINES = [
    ("Strategic Workshop", 1200.0),
    ("Support Retainer", 850.0),
]


def _cleanup(env):
    moves = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        ("ref", "=", INVOICE_REF),
    ])
    for move in moves:
        for payment in move._get_reconciled_payments():
            if payment.state == "posted":
                payment.action_draft()
            payment.unlink()
        if move.state == "posted":
            move.button_draft()
        if move.state == "draft":
            move.button_cancel()
        move.unlink()


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "customer_rank": 1,
            "email": "billing@northwindadvisory.example.com",
        })
    else:
        partner.write({"customer_rank": max(partner.customer_rank, 1)})
    return partner


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "type": "service",
            "list_price": price,
            "invoice_policy": "order",
        })
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "service",
        "list_price": price,
        "invoice_policy": "order",
    })
    return tmpl.product_variant_id


def setup(env):
    _cleanup(env)

    _ensure_partner(env)
    for name, price in LINES:
        _ensure_product(env, name, price)
