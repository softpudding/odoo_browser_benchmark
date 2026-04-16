"""Seed posted customer invoices for the pay_invoice_with_memo task.

Category 2 (MEDIUM): Register a payment on the correct posted invoice with two
non-default wizard fields — memo text and payment date.

The agent must distinguish the target invoice (BENCH-PAYMEMO-01) from a
distractor invoice (BENCH-PAYMEMO-02) for the same customer, and fill in
the memo and payment date instead of accepting defaults.
"""

PARTNER_NAME = "Highfield Consulting"
TARGET_REF = "BENCH-PAYMEMO-01"
DISTRACTOR_REF = "BENCH-PAYMEMO-02"
INVOICE_AMOUNT = 2400.0


def _cleanup(env):
    moves = env["account.move"].search([
        ("ref", "in", [TARGET_REF, DISTRACTOR_REF]),
        ("move_type", "=", "out_invoice"),
    ])
    for move in moves:
        # Cancel any linked payments first
        for payment in move._get_reconciled_payments():
            if payment.state == "posted":
                payment.action_draft()
            payment.unlink()
        if move.state == "posted":
            move.button_draft()
        if move.state == "draft":
            move.button_cancel()
        move.unlink()


def _ensure_partner(env, name):
    partner = env["res.partner"].search([("name", "=", name)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": name,
            "customer_rank": 1,
        })
    return partner


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "invoice_policy": "order",
            "list_price": price,
        })
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "service",
        "invoice_policy": "order",
        "list_price": price,
    })
    return tmpl.product_variant_id


def _make_invoice(env, partner, product, ref, amount):
    journal = env["account.journal"].search(
        [("type", "=", "sale")], limit=1
    )
    invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "journal_id": journal.id,
        "ref": ref,
        "invoice_line_ids": [(0, 0, {
            "product_id": product.id,
            "quantity": 1,
            "price_unit": amount,
            "tax_ids": [(5, 0, 0)],
        })],
    })
    invoice.action_post()
    return invoice


def setup(env):
    _cleanup(env)

    partner = _ensure_partner(env, PARTNER_NAME)
    product = _ensure_product(env, "Consulting Services", INVOICE_AMOUNT)

    _make_invoice(env, partner, product, TARGET_REF, INVOICE_AMOUNT)
    _make_invoice(env, partner, product, DISTRACTOR_REF, INVOICE_AMOUNT)
