"""Seed draft customer invoices for the update-customer-invoice-terms-post task.

Category 2 (MEDIUM): open an existing draft customer invoice, edit a couple of
header fields plus one line quantity, then confirm it without touching a
similarly named distractor invoice.
"""

PARTNER_NAME = "Brightstar Labs"
TARGET_REF = "MED-CINV-01"
DISTRACTOR_REF = "MED-CINV-02"
FINAL_REF = "BRIGHT-READY"


def _cleanup_invoices(env):
    invoices = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        "|",
        ("ref", "in", [TARGET_REF, DISTRACTOR_REF, FINAL_REF]),
        ("invoice_origin", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for invoice in invoices:
        if invoice.state == "posted":
            invoice.button_draft()
        invoice.unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "list_price": price,
            "standard_price": price,
        })
        return product

    template = env["product.template"].create({
        "name": name,
        "type": "service",
        "list_price": price,
        "standard_price": price,
    })
    return template.product_variant_id


def _ensure_payment_term(env):
    term = env["account.payment.term"].search(
        [("name", "=", "30 Net Days")],
        limit=1,
    )
    if term:
        return term

    return env["account.payment.term"].create({
        "name": "30 Net Days",
        "line_ids": [(0, 0, {
            "value": "percent",
            "value_amount": 100,
            "nb_days": 30,
        })],
    })


def _make_invoice(env, partner, ref, support):
    return env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": ref,
        "invoice_origin": ref,
        "invoice_date": "2026-05-01",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": support.id,
                "quantity": 3,
                "price_unit": 450.0,
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })


def setup(env):
    _cleanup_invoices(env)

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "billing@brightstar.example.com",
        })

    _ensure_payment_term(env)
    support = _ensure_product(env, "Support Review", 450.0)
    _make_invoice(env, partner, TARGET_REF, support)
    _make_invoice(env, partner, DISTRACTOR_REF, support)
